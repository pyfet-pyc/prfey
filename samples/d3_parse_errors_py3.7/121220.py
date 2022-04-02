# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\soupsieve\css_match.py
"""CSS matcher."""
from __future__ import unicode_literals
from datetime import datetime
from . import util
import re
from . import css_types as ct
import unicodedata
RE_NOT_EMPTY = re.compile('[^ \t\r\n\x0c]')
RE_NOT_WS = re.compile('[^ \t\r\n\x0c]+')
REL_PARENT = ' '
REL_CLOSE_PARENT = '>'
REL_SIBLING = '~'
REL_CLOSE_SIBLING = '+'
REL_HAS_PARENT = ': '
REL_HAS_CLOSE_PARENT = ':>'
REL_HAS_SIBLING = ':~'
REL_HAS_CLOSE_SIBLING = ':+'
NS_XHTML = 'http://www.w3.org/1999/xhtml'
NS_XML = 'http://www.w3.org/XML/1998/namespace'
DIR_FLAGS = ct.SEL_DIR_LTR | ct.SEL_DIR_RTL
RANGES = ct.SEL_IN_RANGE | ct.SEL_OUT_OF_RANGE
DIR_MAP = {'ltr':ct.SEL_DIR_LTR, 
 'rtl':ct.SEL_DIR_RTL, 
 'auto':0}
RE_NUM = re.compile('^(?P<value>-?(?:[0-9]{1,}(\\.[0-9]+)?|\\.[0-9]+))$')
RE_TIME = re.compile('^(?P<hour>[0-9]{2}):(?P<minutes>[0-9]{2})$')
RE_MONTH = re.compile('^(?P<year>[0-9]{4,})-(?P<month>[0-9]{2})$')
RE_WEEK = re.compile('^(?P<year>[0-9]{4,})-W(?P<week>[0-9]{2})$')
RE_DATE = re.compile('^(?P<year>[0-9]{4,})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})$')
RE_DATETIME = re.compile('^(?P<year>[0-9]{4,})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})T(?P<hour>[0-9]{2}):(?P<minutes>[0-9]{2})$')
RE_WILD_STRIP = re.compile('(?:(?:-\\*-)(?:\\*(?:-|$))*|-\\*$)')
MONTHS_30 = (4, 6, 9, 11)
FEB = 2
SHORT_MONTH = 30
LONG_MONTH = 31
FEB_MONTH = 28
FEB_LEAP_MONTH = 29
DAYS_IN_WEEK = 7

class _FakeParent(object):
    __doc__ = "\n    Fake parent class.\n\n    When we have a fragment with no `BeautifulSoup` document object,\n    we can't evaluate `nth` selectors properly.  Create a temporary\n    fake parent so we can traverse the root element as a child.\n    "

    def __init__(self, element):
        """Initialize."""
        self.contents = [
         element]

    def __len__(self):
        """Length."""
        return len(self.contents)


class _DocumentNav(object):
    __doc__ = 'Navigate a Beautiful Soup document.'

    @classmethod
    def assert_valid_input(cls, tag):
        """Check if valid input tag or document."""
        if not cls.is_tag(tag):
            raise TypeError("Expected a BeautifulSoup 'Tag', but instead recieved type {}".format(type(tag)))

    @staticmethod
    def is_doc(obj):
        """Is `BeautifulSoup` object."""
        import bs4
        return isinstance(obj, bs4.BeautifulSoup)

    @staticmethod
    def is_tag(obj):
        """Is tag."""
        import bs4
        return isinstance(obj, bs4.Tag)

    @staticmethod
    def is_comment(obj):
        """Is comment."""
        import bs4
        return isinstance(obj, bs4.Comment)

    @staticmethod
    def is_declaration(obj):
        """Is declaration."""
        import bs4
        return isinstance(obj, bs4.Declaration)

    @staticmethod
    def is_cdata(obj):
        """Is CDATA."""
        import bs4
        return isinstance(obj, bs4.CData)

    @staticmethod
    def is_processing_instruction(obj):
        """Is processing instruction."""
        import bs4
        return isinstance(obj, bs4.ProcessingInstruction)

    @staticmethod
    def is_navigable_string(obj):
        """Is navigable string."""
        import bs4
        return isinstance(obj, bs4.NavigableString)

    @staticmethod
    def is_special_string(obj):
        """Is special string."""
        import bs4
        return isinstance(obj, (bs4.Comment, bs4.Declaration, bs4.CData, bs4.ProcessingInstruction, bs4.Doctype))

    @classmethod
    def is_content_string(cls, obj):
        """Check if node is content string."""
        return cls.is_navigable_string(obj) and not cls.is_special_string(obj)

    @staticmethod
    def create_fake_parent(el):
        """Create fake parent for a given element."""
        return _FakeParent(el)

    @staticmethod
    def is_xml_tree(el):
        """Check if element (or document) is from a XML tree."""
        return el._is_xml

    def is_iframe(self, el):
        """Check if element is an `iframe`."""
        return (el.name if self.is_xml_tree(el) else util.lower(el.name)) == 'iframe' and self.is_html_tag(el)

    def is_root(self, el):
        """
        Return whether element is a root element.

        We check that the element is the root of the tree (which we have already pre-calculated),
        and we check if it is the root element under an `iframe`.
        """
        root = self.root and self.root is el
        if not root:
            parent = self.get_parent(el)
            root = parent is not None and self.is_html and self.is_iframe(parent)
        return root

    def get_contents(self, el, no_iframe=False):
        """Get contents or contents in reverse."""
        if not (no_iframe and self.is_iframe(el)):
            for content in el.contents:
                yield content

    def get_children(self, el, start=None, reverse=False, tags=True, no_iframe=False):
        """Get children."""
        if not (no_iframe and self.is_iframe(el)):
            last = len(el.contents) - 1
            if start is None:
                index = last if reverse else 0
            else:
                index = start
            end = -1 if reverse else last + 1
            incr = -1 if reverse else 1
            if 0 <= index <= last:
                while index != end:
                    node = el.contents[index]
                    index += incr
                    if tags:
                        if self.is_tag(node):
                            pass
                        yield node

    def get_descendants(self, el, tags=True, no_iframe=False):
        """Get descendants."""
        if not (no_iframe and self.is_iframe(el)):
            next_good = None
            for child in el.descendants:
                if next_good is not None:
                    if child is not next_good:
                        continue
                    else:
                        next_good = None
                else:
                    is_tag = self.is_tag(child)
                if no_iframe:
                    if is_tag:
                        if self.is_iframe(child):
                            if child.next_sibling is not None:
                                next_good = child.next_sibling
                            else:
                                last_child = child
                                while self.is_tag(last_child):
                                    if last_child.contents:
                                        last_child = last_child.contents[(-1)]

                                next_good = last_child.next_element
                            yield child
                            if next_good is None:
                                break
                            if tags:
                                if is_tag:
                                    pass
                                yield child

    def get_parent(self, el, no_iframe=False):
        """Get parent."""
        parent = el.parent
        if no_iframe:
            if parent is not None:
                if self.is_iframe(parent):
                    parent = None
        return parent

    @staticmethod
    def get_tag_name(el):
        """Get tag."""
        return el.name

    @staticmethod
    def get_prefix_name(el):
        """Get prefix."""
        return el.prefix

    @staticmethod
    def get_uri(el):
        """Get namespace `URI`."""
        return el.namespace

    @classmethod
    def get_next(cls, el, tags=True):
        """Get next sibling tag."""
        sibling = el.next_sibling
        while tags:
            if not cls.is_tag(sibling):
                if sibling is not None:
                    sibling = sibling.next_sibling

        return sibling

    @classmethod
    def get_previous(cls, el, tags=True):
        """Get previous sibling tag."""
        sibling = el.previous_sibling
        while tags:
            if not cls.is_tag(sibling):
                if sibling is not None:
                    sibling = sibling.previous_sibling

        return sibling

    @staticmethod
    def has_html_ns(el):
        """
        Check if element has an HTML namespace.

        This is a bit different than whether a element is treated as having an HTML namespace,
        like we do in the case of `is_html_tag`.
        """
        ns = getattr(el, 'namespace') if el else None
        return ns and ns == NS_XHTML

    @staticmethod
    def split_namespace(el, attr_name):
        """Return namespace and attribute name without the prefix."""
        return (
         getattr(attr_name, 'namespace', None), getattr(attr_name, 'name', None))

    @staticmethod
    def get_attribute_by_name(el, name, default=None):
        """Get attribute by name."""
        value = default
        if el._is_xml:
            try:
                value = el.attrs[name]
            except KeyError:
                pass

        else:
            for k, v in el.attrs.items():
                if util.lower(k) == name:
                    value = v
                    break

        return value

    @staticmethod
    def iter_attributes(el):
        """Iterate attributes."""
        for k, v in el.attrs.items():
            yield (
             k, v)

    @classmethod
    def get_classes(cls, el):
        """Get classes."""
        classes = cls.get_attribute_by_name(el, 'class', [])
        if isinstance(classes, util.ustr):
            classes = RE_NOT_WS.findall(classes)
        return classes

    def get_text(self, el, no_iframe=False):
        """Get text."""
        return ''.join([node for node in self.get_descendants(el, tags=False, no_iframe=no_iframe) if self.is_content_string(node)])


class Inputs(object):
    __doc__ = 'Class for parsing and validating input items.'

    @staticmethod
    def validate_day(year, month, day):
        """Validate day."""
        max_days = LONG_MONTH
        if month == FEB:
            max_days = FEB_LEAP_MONTH if not ((year % 4 == 0) and (year % 100 != 0)) and (year % 400 == 0) else FEB_MONTH
        elif month in MONTHS_30:
            max_days = SHORT_MONTH
        return 1 <= day <= max_days

    @staticmethod
    def validate_week(year, week):
        """Validate week."""
        max_week = datetime.strptime('{}-{}-{}'.format(12, 31, year), '%m-%d-%Y').isocalendar()[1]
        if max_week == 1:
            max_week = 53
        return 1 <= week <= max_week

    @staticmethod
    def validate_month(month):
        """Validate month."""
        return 1 <= month <= 12

    @staticmethod
    def validate_year(year):
        """Validate year."""
        return 1 <= year

    @staticmethod
    def validate_hour(hour):
        """Validate hour."""
        return 0 <= hour <= 23

    @staticmethod
    def validate_minutes(minutes):
        """Validate minutes."""
        return 0 <= minutes <= 59

    @classmethod
    def parse_value(cls, itype, value):
        """Parse the input value."""
        parsed = None
        if itype == 'date':
            m = RE_DATE.match(value)
            if m:
                year = int(m.group('year'), 10)
                month = int(m.group('month'), 10)
                day = int(m.group('day'), 10)
                if cls.validate_year(year):
                    if cls.validate_month(month):
                        if cls.validate_day(year, month, day):
                            parsed = (
                             year, month, day)
        elif itype == 'month':
            m = RE_MONTH.match(value)
            if m:
                year = int(m.group('year'), 10)
                month = int(m.group('month'), 10)
                if cls.validate_year(year):
                    if cls.validate_month(month):
                        parsed = (
                         year, month)
        elif itype == 'week':
            m = RE_WEEK.match(value)
            if m:
                year = int(m.group('year'), 10)
                week = int(m.group('week'), 10)
                if not cls.validate_year(year) or cls.validate_week(year, week):
                    parsed = (
                     year, week)
        elif itype == 'time':
            m = RE_TIME.match(value)
            if m:
                hour = int(m.group('hour'), 10)
                minutes = int(m.group('minutes'), 10)
                if not cls.validate_hour(hour) or cls.validate_minutes(minutes):
                    parsed = (
                     hour, minutes)
        elif itype == 'datetime-local':
            m = RE_DATETIME.match(value)
            if m:
                year = int(m.group('year'), 10)
                month = int(m.group('month'), 10)
                day = int(m.group('day'), 10)
                hour = int(m.group('hour'), 10)
                minutes = int(m.group('minutes'), 10)
                if cls.validate_year(year):
                    if cls.validate_month(month):
                        if cls.validate_day(year, month, day):
                            if not cls.validate_hour(hour) or cls.validate_minutes(minutes):
                                parsed = (year, month, day, hour, minutes)
        elif itype in ('number', 'range'):
            m = RE_NUM.match(value)
            if m:
                parsed = float(m.group('value'))
        return parsed


class _Match(object):
    __doc__ = 'Perform CSS matching.'

    def __init__(self, selectors, scope, namespaces, flags):
        """Initialize."""
        self.assert_valid_input(scope)
        self.tag = scope
        self.cached_meta_lang = []
        self.cached_default_forms = []
        self.cached_indeterminate_forms = []
        self.selectors = selectors
        self.namespaces = {} if namespaces is None else namespaces
        self.flags = flags
        self.iframe_restrict = False
        doc = scope
        parent = self.get_parent(doc)
        while parent:
            doc = parent
            parent = self.get_parent(doc)

        root = None
        if not self.is_doc(doc):
            root = doc
        else:
            for child in self.get_children(doc):
                root = child
                break

        self.root = root
        self.scope = scope if scope is not doc else root
        self.has_html_namespace = self.has_html_ns(root)
        self.is_xml = self.is_xml_tree(doc)
        self.is_html = not self.is_xml or self.has_html_namespace

    def supports_namespaces(self):
        """Check if namespaces are supported in the HTML type."""
        return self.is_xml or self.has_html_namespace

    def get_tag_ns(self, el):
        """Get tag namespace."""
        if self.supports_namespaces():
            namespace = ''
            ns = self.get_uri(el)
            if ns:
                namespace = ns
        else:
            namespace = NS_XHTML
        return namespace

    def is_html_tag(self, el):
        """Check if tag is in HTML namespace."""
        return self.get_tag_ns(el) == NS_XHTML

    def get_tag(self, el):
        """Get tag."""
        name = self.get_tag_name(el)
        if name is not None:
            if not self.is_xml:
                return util.lower(name)
            return name

    def get_prefix(self, el):
        """Get prefix."""
        prefix = self.get_prefix_name(el)
        if prefix is not None:
            if not self.is_xml:
                return util.lower(prefix)
            return prefix

    def find_bidi(self, el):
        """Get directionality from element text."""
        for node in self.get_children(el, tags=False):
            if self.is_tag(node):
                direction = DIR_MAP.get(util.lower(self.get_attribute_by_name(node, 'dir', '')), None)
                if not self.get_tag(node) in ('bdi', 'script', 'style', 'textarea',
                                              'iframe'):
                    if self.is_html_tag(node):
                        if direction is not None:
                            continue
                        else:
                            value = self.find_bidi(node)
                        if value is not None:
                            return value
                            continue
                        if self.is_special_string(node):
                            continue
                        else:
                            for c in node:
                                bidi = unicodedata.bidirectional(c)
                                if bidi in ('AL', 'R', 'L'):
                                    if bidi == 'L':
                                        return ct.SEL_DIR_LTR
                                    else:
                                        return ct.SEL_DIR_RTL

    def extended_language_filter(self, lang_range, lang_tag):
        """Filter the language tags."""
        match = True
        lang_range = RE_WILD_STRIP.sub('-', lang_range).lower()
        ranges = lang_range.split('-')
        subtags = lang_tag.lower().split('-')
        length = len(ranges)
        rindex = 0
        sindex = 0
        r = ranges[rindex]
        s = subtags[sindex]
        if r != '*':
            if r != s:
                match = False
        rindex += 1
        sindex += 1
        while match:
            if rindex < length:
                r = ranges[rindex]
                try:
                    s = subtags[sindex]
                except IndexError:
                    match = False
                    continue

                if not r:
                    match = False
                    continue
                else:
                    if s == r:
                        rindex += 1
                    else:
                        if len(s) == 1:
                            match = False
                            continue
                sindex += 1

        return match

    def match_attribute_name(self, el, attr, prefix):
        """Match attribute name and return value if it exists."""
        value = None
        if self.supports_namespaces():
            value = None
            if prefix:
                ns = self.namespaces.get(prefix)
                if ns is None:
                    if prefix != '*':
                        return
            else:
                ns = None
            for k, v in self.iter_attributes(el):
                namespace, name = self.split_namespace(el, k)
                if ns is None:
                    if not (self.is_xml and attr == k):
                        if not self.is_xml:
                            if util.lower(attr) == util.lower(k):
                                pass
                            value = v
                            break
                if not namespace is None:
                    if ns != namespace:
                        if prefix != '*':
                            continue
                    if not self.is_xml or util.lower(attr) != util.lower(name):
                        pass
                    else:
                        if attr != name:
                            continue
                value = v
                break

        else:
            for k, v in self.iter_attributes(el):
                if util.lower(attr) != util.lower(k):
                    continue
                else:
                    value = v
                break

        return value

    def match_namespace(self, el, tag):
        """Match the namespace of the element."""
        match = True
        namespace = self.get_tag_ns(el)
        default_namespace = self.namespaces.get('')
        tag_ns = '' if tag.prefix is None else self.namespaces.get(tag.prefix, None)
        if tag.prefix is None and default_namespace is not None and namespace != default_namespace:
            match = False
        elif tag.prefix is not None and tag.prefix == '' and namespace:
            match = False
        else:
            pass
        if not tag.prefix or tag.prefix != '*':
            if tag_ns is None or (namespace != tag_ns):
                match = False
            return match

    def match_attributes(self, el, attributes):
        """Match attributes."""
        match = True
        if attributes:
            for a in attributes:
                value = self.match_attribute_name(el, a.attribute, a.prefix)
                if self.is_xml:
                    pattern = a.xml_type_pattern if a.xml_type_pattern else a.pattern
                    if isinstance(value, list):
                        value = ' '.join(value)
                    if value is None:
                        match = False
                        break
                    else:
                        if pattern is None:
                            continue
                    if pattern.match(value) is None:
                        match = False
                        break

        return match

    def match_tagname(self, el, tag):
        """Match tag name."""
        if not self.is_xml:
            name = util.lower(tag.name) if tag.name is not None else tag.name
            return not (name is not None and name not in (self.get_tag(el), '*'))

    def match_tag(self, el, tag):
        """Match the tag."""
        match = True
        if tag is not None:
            if not self.match_namespace(el, tag):
                match = False
            if not self.match_tagname(el, tag):
                match = False
            return match

    def match_past_relations(self, el, relation):
        """Match past relationship."""
        found = False
        if relation[0].rel_type == REL_PARENT:
            parent = self.get_parent(el, no_iframe=(self.iframe_restrict))
            while not found or parent:
                found = self.match_selectors(parent, relation)
                parent = self.get_parent(parent, no_iframe=(self.iframe_restrict))

        elif relation[0].rel_type == REL_CLOSE_PARENT:
            parent = self.get_parent(el, no_iframe=(self.iframe_restrict))
            if parent:
                found = self.match_selectors(parent, relation)
        elif relation[0].rel_type == REL_SIBLING:
            sibling = self.get_previous(el)
            while not found or sibling:
                found = self.match_selectors(sibling, relation)
                sibling = self.get_previous(sibling)

        elif relation[0].rel_type == REL_CLOSE_SIBLING:
            sibling = self.get_previous(el)
            if sibling:
                if self.is_tag(sibling):
                    found = self.match_selectors(sibling, relation)
        return found

    def match_future_child(self, parent, relation, recursive=False):
        """Match future child."""
        match = False
        children = self.get_descendants if recursive else self.get_children
        for child in children(parent, no_iframe=(self.iframe_restrict)):
            match = self.match_selectors(child, relation)
            if match:
                break

        return match

    def match_future_relations(self, el, relation):
        """Match future relationship."""
        found = False
        if relation[0].rel_type == REL_HAS_PARENT:
            found = self.match_future_child(el, relation, True)
        elif relation[0].rel_type == REL_HAS_CLOSE_PARENT:
            found = self.match_future_child(el, relation)
        elif relation[0].rel_type == REL_HAS_SIBLING:
            sibling = self.get_next(el)
            while not found or sibling:
                found = self.match_selectors(sibling, relation)
                sibling = self.get_next(sibling)

        elif relation[0].rel_type == REL_HAS_CLOSE_SIBLING:
            sibling = self.get_next(el)
            if sibling:
                if self.is_tag(sibling):
                    found = self.match_selectors(sibling, relation)
        return found

    def match_relations(self, el, relation):
        """Match relationship to other elements."""
        found = False
        if relation[0].rel_type.startswith(':'):
            found = self.match_future_relations(el, relation)
        else:
            found = self.match_past_relations(el, relation)
        return found

    def match_id(self, el, ids):
        """Match element's ID."""
        found = True
        for i in ids:
            if i != self.get_attribute_by_name(el, 'id', ''):
                found = False
                break

        return found

    def match_classes(self, el, classes):
        """Match element's classes."""
        current_classes = self.get_classes(el)
        found = True
        for c in classes:
            if c not in current_classes:
                found = False
                break

        return found

    def match_root(self, el):
        """Match element as root."""
        is_root = self.is_root(el)
        if is_root:
            sibling = self.get_previous(el, tags=False)
            while is_root:
                if sibling is not None:
                    if not self.is_tag(sibling):
                        if not (self.is_content_string(sibling) and sibling.strip()):
                            if self.is_cdata(sibling):
                                is_root = False
                            else:
                                sibling = self.get_previous(sibling, tags=False)

        if is_root:
            sibling = self.get_next(el, tags=False)
            while is_root:
                if sibling is not None:
                    if not self.is_tag(sibling):
                        if not (self.is_content_string(sibling) and sibling.strip()):
                            if self.is_cdata(sibling):
                                is_root = False
                            else:
                                sibling = self.get_next(sibling, tags=False)

        return is_root

    def match_scope(self, el):
        """Match element as scope."""
        return self.scope is el

    def match_nth_tag_type(self, el, child):
        """Match tag type for `nth` matches."""
        return self.get_tag(child) == self.get_tag(el) and self.get_tag_ns(child) == self.get_tag_ns(el)

    def match_nth(self, el, nth):
        """Match `nth` elements."""
        matched = True
        for n in nth:
            matched = False
            if n.selectors:
                if not self.match_selectors(el, n.selectors):
                    break
                parent = self.get_parent(el)
                if parent is None:
                    parent = self.create_fake_parent(el)
                else:
                    last = n.last
                    last_index = len(parent) - 1
                    index = last_index if last else 0
                    relative_index = 0
                    a = n.a
                    b = n.b
                    var = n.n
                    count = 0
                    count_incr = 1
                    factor = -1 if last else 1
                    idx = last_idx = a * count + b if var else a
                    if var:
                        adjust = None
                        while idx < 1 or idx > last_index:
                            if idx < 0:
                                diff_low = 0 - idx
                                if adjust is not None:
                                    if adjust == 1:
                                        break
                                adjust = -1
                                count += count_incr
                                idx = last_idx = a * count + b if var else a
                                diff = 0 - idx
                                if diff >= diff_low:
                                    break
                            else:
                                diff_high = idx - last_index
                                if adjust is not None:
                                    if adjust == -1:
                                        break
                                adjust = 1
                                count += count_incr
                                idx = last_idx = a * count + b if var else a
                                diff = idx - last_index
                                if diff >= diff_high:
                                    break
                                else:
                                    diff_high = diff

                        lowest = count
                        if a < 0:
                            while idx >= 1:
                                lowest = count
                                count += count_incr
                                idx = last_idx = a * count + b if var else a

                            count_incr = -1
                        count = lowest
                        idx = last_idx = a * count + b if var else a
                    while 1 <= idx <= last_index + 1:
                        child = None
                        for child in self.get_children(parent, start=index, reverse=(factor < 0), tags=False):
                            index += factor
                            if not self.is_tag(child):
                                continue
                            if n.selectors:
                                if not self.match_selectors(child, n.selectors):
                                    continue
                                if n.of_type:
                                    if not self.match_nth_tag_type(el, child):
                                        continue
                                    relative_index += 1
                                    if relative_index == idx:
                                        if child is el:
                                            matched = True
                                        else:
                                            break
                                    if child is el:
                                        break

                        if child is el:
                            break
                        else:
                            last_idx = idx
                            count += count_incr
                        if count < 0:
                            break
                        else:
                            idx = a * count + b if var else a
                        if last_idx == idx:
                            break

                if not matched:
                    break

        return matched

    def match_empty(self, el):
        """Check if element is empty (if requested)."""
        is_empty = True
        for child in self.get_children(el, tags=False):
            if self.is_tag(child):
                is_empty = False
                break
            if self.is_content_string(child):
                if RE_NOT_EMPTY.search(child):
                    is_empty = False
                    break

        return is_empty

    def match_subselectors(self, el, selectors):
        """Match selectors."""
        match = True
        for sel in selectors:
            if not self.match_selectors(el, sel):
                match = False

        return match

    def match_contains(self, el, contains):
        """Match element if it contains text."""
        match = True
        content = None
        for contain_list in contains:
            if content is None:
                content = self.get_text(el, no_iframe=(self.is_html))
            else:
                found = False
                for text in contain_list.text:
                    if text in content:
                        found = True
                        break

            if not found:
                match = False

        return match

    def match_default(self, el):
        """Match default."""
        match = False
        form = None
        parent = self.get_parent(el, no_iframe=True)
        while parent:
            if form is None:
                if self.get_tag(parent) == 'form' and self.is_html_tag(parent):
                    form = parent
                else:
                    parent = self.get_parent(parent, no_iframe=True)

        found_form = False
        for f, t in self.cached_default_forms:
            if f is form:
                found_form = True
                if t is el:
                    match = True
                break

        if not found_form:
            for child in self.get_descendants(form, no_iframe=True):
                name = self.get_tag(child)
                if name == 'form':
                    break
                if name in ('input', 'button'):
                    v = self.get_attribute_by_name(child, 'type', '')
                    if v:
                        if util.lower(v) == 'submit':
                            self.cached_default_forms.append([form, child])
                            if el is child:
                                match = True
                            break

        return match

    def match_indeterminate(self, el):
        """Match default."""
        match = False
        name = self.get_attribute_by_name(el, 'name')

        def get_parent_form(el):
            form = None
            parent = self.get_parent(el, no_iframe=True)
            while form is None:
                if self.get_tag(parent) == 'form':
                    if self.is_html_tag(parent):
                        form = parent
                        break
                last_parent = parent
                parent = self.get_parent(parent, no_iframe=True)
                if parent is None:
                    form = last_parent
                    break

            return form

        form = get_parent_form(el)
        found_form = False
        for f, n, i in self.cached_indeterminate_forms:
            if f is form:
                if n == name:
                    found_form = True
                    if i is True:
                        match = True
                    break

        if not found_form:
            checked = False
            for child in self.get_descendants(form, no_iframe=True):
                if child is el:
                    continue
                else:
                    tag_name = self.get_tag(child)
                    if tag_name == 'input':
                        is_radio = False
                        check = False
                        has_name = False
                        for k, v in self.iter_attributes(child):
                            if util.lower(k) == 'type' and util.lower(v) == 'radio':
                                is_radio = True
                            elif util.lower(k) == 'name' and v == name:
                                has_name = True
                            elif util.lower(k) == 'checked':
                                check = True
                            if is_radio:
                                if check:
                                    if has_name:
                                        if get_parent_form(child) is form:
                                            checked = True
                                            break

                if checked:
                    break

            if not checked:
                match = True
            self.cached_indeterminate_forms.append([form, name, match])
        return match

    def match_lang--- This code section failed: ---

 L.1079         0  LOAD_CONST               False
                2  STORE_FAST               'match'

 L.1080         4  LOAD_FAST                'self'
                6  LOAD_METHOD              supports_namespaces
                8  CALL_METHOD_0         0  '0 positional arguments'
               10  STORE_FAST               'has_ns'

 L.1081        12  LOAD_FAST                'self'
               14  LOAD_ATTR                root
               16  STORE_FAST               'root'

 L.1082        18  LOAD_FAST                'self'
               20  LOAD_ATTR                has_html_namespace
               22  STORE_FAST               'has_html_namespace'

 L.1085        24  LOAD_FAST                'el'
               26  STORE_FAST               'parent'

 L.1086        28  LOAD_CONST               None
               30  STORE_FAST               'found_lang'

 L.1087        32  LOAD_CONST               None
               34  STORE_FAST               'last'

 L.1088        36  SETUP_LOOP          230  'to 230'
             38_0  COME_FROM           226  '226'
             38_1  COME_FROM           204  '204'
               38  LOAD_FAST                'found_lang'
               40  POP_JUMP_IF_TRUE    228  'to 228'

 L.1089        42  LOAD_FAST                'self'
               44  LOAD_METHOD              has_html_ns
               46  LOAD_FAST                'parent'
               48  CALL_METHOD_1         1  '1 positional argument'
               50  STORE_FAST               'has_html_ns'

 L.1090        52  SETUP_LOOP          178  'to 178'
               54  LOAD_FAST                'self'
               56  LOAD_METHOD              iter_attributes
               58  LOAD_FAST                'parent'
               60  CALL_METHOD_1         1  '1 positional argument'
               62  GET_ITER         
             64_0  COME_FROM           174  '174'
             64_1  COME_FROM           166  '166'
             64_2  COME_FROM           134  '134'
             64_3  COME_FROM           126  '126'
             64_4  COME_FROM           122  '122'
               64  FOR_ITER            176  'to 176'
               66  UNPACK_SEQUENCE_2     2 
               68  STORE_FAST               'k'
               70  STORE_FAST               'v'

 L.1091        72  LOAD_FAST                'self'
               74  LOAD_METHOD              split_namespace
               76  LOAD_FAST                'parent'
               78  LOAD_FAST                'k'
               80  CALL_METHOD_2         2  '2 positional arguments'
               82  UNPACK_SEQUENCE_2     2 
               84  STORE_FAST               'attr_ns'
               86  STORE_FAST               'attr'

 L.1093        88  LOAD_FAST                'has_ns'
               90  POP_JUMP_IF_FALSE    96  'to 96'
               92  LOAD_FAST                'has_html_ns'
               94  POP_JUMP_IF_FALSE   120  'to 120'
             96_0  COME_FROM            90  '90'
               96  LOAD_FAST                'self'
               98  LOAD_ATTR                is_xml
              100  POP_JUMP_IF_TRUE    112  'to 112'
              102  LOAD_GLOBAL              util
              104  LOAD_METHOD              lower
              106  LOAD_FAST                'k'
              108  CALL_METHOD_1         1  '1 positional argument'
              110  JUMP_FORWARD        114  'to 114'
            112_0  COME_FROM           100  '100'
              112  LOAD_FAST                'k'
            114_0  COME_FROM           110  '110'
              114  LOAD_STR                 'lang'
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_TRUE    168  'to 168'
            120_0  COME_FROM            94  '94'

 L.1095       120  LOAD_FAST                'has_ns'
              122  POP_JUMP_IF_FALSE_BACK    64  'to 64'
              124  LOAD_FAST                'has_html_ns'
              126  POP_JUMP_IF_TRUE_BACK    64  'to 64'
              128  LOAD_FAST                'attr_ns'
              130  LOAD_GLOBAL              NS_XML
              132  COMPARE_OP               ==
              134  POP_JUMP_IF_FALSE_BACK    64  'to 64'

 L.1096       136  LOAD_FAST                'self'
              138  LOAD_ATTR                is_xml
              140  POP_JUMP_IF_TRUE    160  'to 160'
              142  LOAD_FAST                'attr'
              144  LOAD_CONST               None
              146  COMPARE_OP               is-not
              148  POP_JUMP_IF_FALSE   160  'to 160'
              150  LOAD_GLOBAL              util
              152  LOAD_METHOD              lower
              154  LOAD_FAST                'attr'
              156  CALL_METHOD_1         1  '1 positional argument'
              158  JUMP_FORWARD        162  'to 162'
            160_0  COME_FROM           148  '148'
            160_1  COME_FROM           140  '140'
              160  LOAD_FAST                'attr'
            162_0  COME_FROM           158  '158'
              162  LOAD_STR                 'lang'
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_FALSE_BACK    64  'to 64'
            168_0  COME_FROM           118  '118'

 L.1099       168  LOAD_FAST                'v'
              170  STORE_FAST               'found_lang'

 L.1100       172  BREAK_LOOP       
              174  JUMP_BACK            64  'to 64'
              176  POP_BLOCK        
            178_0  COME_FROM_LOOP       52  '52'

 L.1101       178  LOAD_FAST                'parent'
              180  STORE_FAST               'last'

 L.1102       182  LOAD_FAST                'self'
              184  LOAD_ATTR                get_parent
              186  LOAD_FAST                'parent'
              188  LOAD_FAST                'self'
              190  LOAD_ATTR                is_html
              192  LOAD_CONST               ('no_iframe',)
              194  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              196  STORE_FAST               'parent'

 L.1104       198  LOAD_FAST                'parent'
              200  LOAD_CONST               None
              202  COMPARE_OP               is
              204  POP_JUMP_IF_FALSE_BACK    38  'to 38'

 L.1105       206  LOAD_FAST                'last'
              208  STORE_FAST               'root'

 L.1106       210  LOAD_FAST                'self'
              212  LOAD_METHOD              has_html_ns
              214  LOAD_FAST                'root'
              216  CALL_METHOD_1         1  '1 positional argument'
              218  STORE_FAST               'has_html_namespace'

 L.1107       220  LOAD_FAST                'last'
              222  STORE_FAST               'parent'

 L.1108       224  BREAK_LOOP       
              226  JUMP_BACK            38  'to 38'
            228_0  COME_FROM            40  '40'
              228  POP_BLOCK        
            230_0  COME_FROM_LOOP       36  '36'

 L.1111       230  LOAD_FAST                'found_lang'
          232_234  POP_JUMP_IF_TRUE    280  'to 280'
              236  LOAD_FAST                'self'
              238  LOAD_ATTR                cached_meta_lang
          240_242  POP_JUMP_IF_FALSE   280  'to 280'

 L.1112       244  SETUP_LOOP          280  'to 280'
              246  LOAD_FAST                'self'
              248  LOAD_ATTR                cached_meta_lang
              250  GET_ITER         
            252_0  COME_FROM           276  '276'
            252_1  COME_FROM           266  '266'
              252  FOR_ITER            278  'to 278'
              254  STORE_FAST               'cache'

 L.1113       256  LOAD_FAST                'root'
              258  LOAD_FAST                'cache'
              260  LOAD_CONST               0
              262  BINARY_SUBSCR    
              264  COMPARE_OP               is
              266  POP_JUMP_IF_FALSE_BACK   252  'to 252'

 L.1114       268  LOAD_FAST                'cache'
              270  LOAD_CONST               1
              272  BINARY_SUBSCR    
              274  STORE_FAST               'found_lang'
              276  JUMP_BACK           252  'to 252'
              278  POP_BLOCK        
            280_0  COME_FROM_LOOP      244  '244'
            280_1  COME_FROM           240  '240'
            280_2  COME_FROM           232  '232'

 L.1117       280  LOAD_FAST                'found_lang'
              282  LOAD_CONST               None
              284  COMPARE_OP               is
          286_288  POP_JUMP_IF_FALSE   630  'to 630'
              290  LOAD_FAST                'self'
              292  LOAD_ATTR                is_xml
          294_296  POP_JUMP_IF_FALSE   316  'to 316'
              298  LOAD_FAST                'has_html_namespace'
          300_302  POP_JUMP_IF_FALSE   630  'to 630'
              304  LOAD_FAST                'root'
              306  LOAD_ATTR                name
              308  LOAD_STR                 'html'
              310  COMPARE_OP               ==
          312_314  POP_JUMP_IF_FALSE   630  'to 630'
            316_0  COME_FROM           294  '294'

 L.1119       316  LOAD_CONST               False
              318  STORE_FAST               'found'

 L.1120       320  SETUP_LOOP          414  'to 414'
              322  LOAD_CONST               ('html', 'head')
              324  GET_ITER         
            326_0  COME_FROM           408  '408'
            326_1  COME_FROM           402  '402'
              326  FOR_ITER            412  'to 412'
              328  STORE_FAST               'tag'

 L.1121       330  LOAD_CONST               False
              332  STORE_FAST               'found'

 L.1122       334  SETUP_LOOP          400  'to 400'
              336  LOAD_FAST                'self'
              338  LOAD_ATTR                get_children
              340  LOAD_FAST                'parent'
              342  LOAD_FAST                'self'
              344  LOAD_ATTR                is_html
              346  LOAD_CONST               ('no_iframe',)
              348  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              350  GET_ITER         
            352_0  COME_FROM           394  '394'
            352_1  COME_FROM           380  '380'
            352_2  COME_FROM           368  '368'
              352  FOR_ITER            398  'to 398'
              354  STORE_FAST               'child'

 L.1123       356  LOAD_FAST                'self'
              358  LOAD_METHOD              get_tag
              360  LOAD_FAST                'child'
              362  CALL_METHOD_1         1  '1 positional argument'
              364  LOAD_FAST                'tag'
              366  COMPARE_OP               ==
          368_370  POP_JUMP_IF_FALSE_BACK   352  'to 352'
              372  LOAD_FAST                'self'
              374  LOAD_METHOD              is_html_tag
              376  LOAD_FAST                'child'
              378  CALL_METHOD_1         1  '1 positional argument'
          380_382  POP_JUMP_IF_FALSE_BACK   352  'to 352'

 L.1124       384  LOAD_CONST               True
              386  STORE_FAST               'found'

 L.1125       388  LOAD_FAST                'child'
              390  STORE_FAST               'parent'

 L.1126       392  BREAK_LOOP       
          394_396  JUMP_BACK           352  'to 352'
              398  POP_BLOCK        
            400_0  COME_FROM_LOOP      334  '334'

 L.1127       400  LOAD_FAST                'found'
          402_404  POP_JUMP_IF_TRUE_BACK   326  'to 326'

 L.1128       406  BREAK_LOOP       
          408_410  JUMP_BACK           326  'to 326'
              412  POP_BLOCK        
            414_0  COME_FROM_LOOP      320  '320'

 L.1131       414  LOAD_FAST                'found'
          416_418  POP_JUMP_IF_FALSE   630  'to 630'

 L.1132       420  SETUP_LOOP          608  'to 608'
              422  LOAD_FAST                'parent'
              424  GET_ITER         
            426_0  COME_FROM           602  '602'
            426_1  COME_FROM           596  '596'
              426  FOR_ITER            606  'to 606'
              428  STORE_FAST               'child'

 L.1133       430  LOAD_FAST                'self'
              432  LOAD_METHOD              is_tag
              434  LOAD_FAST                'child'
              436  CALL_METHOD_1         1  '1 positional argument'
          438_440  POP_JUMP_IF_FALSE   594  'to 594'
              442  LOAD_FAST                'self'
              444  LOAD_METHOD              get_tag
              446  LOAD_FAST                'child'
              448  CALL_METHOD_1         1  '1 positional argument'
              450  LOAD_STR                 'meta'
              452  COMPARE_OP               ==
          454_456  POP_JUMP_IF_FALSE   594  'to 594'
              458  LOAD_FAST                'self'
              460  LOAD_METHOD              is_html_tag
              462  LOAD_FAST                'parent'
              464  CALL_METHOD_1         1  '1 positional argument'
          466_468  POP_JUMP_IF_FALSE   594  'to 594'

 L.1134       470  LOAD_CONST               False
              472  STORE_FAST               'c_lang'

 L.1135       474  LOAD_CONST               None
              476  STORE_FAST               'content'

 L.1136       478  SETUP_LOOP          594  'to 594'
              480  LOAD_FAST                'self'
              482  LOAD_METHOD              iter_attributes
              484  LOAD_FAST                'child'
              486  CALL_METHOD_1         1  '1 positional argument'
              488  GET_ITER         
            490_0  COME_FROM           588  '588'
            490_1  COME_FROM           562  '562'
            490_2  COME_FROM           556  '556'
              490  FOR_ITER            592  'to 592'
              492  UNPACK_SEQUENCE_2     2 
              494  STORE_FAST               'k'
              496  STORE_FAST               'v'

 L.1137       498  LOAD_GLOBAL              util
              500  LOAD_METHOD              lower
              502  LOAD_FAST                'k'
              504  CALL_METHOD_1         1  '1 positional argument'
              506  LOAD_STR                 'http-equiv'
              508  COMPARE_OP               ==
          510_512  POP_JUMP_IF_FALSE   534  'to 534'
              514  LOAD_GLOBAL              util
              516  LOAD_METHOD              lower
              518  LOAD_FAST                'v'
              520  CALL_METHOD_1         1  '1 positional argument'
              522  LOAD_STR                 'content-language'
              524  COMPARE_OP               ==
          526_528  POP_JUMP_IF_FALSE   534  'to 534'

 L.1138       530  LOAD_CONST               True
              532  STORE_FAST               'c_lang'
            534_0  COME_FROM           526  '526'
            534_1  COME_FROM           510  '510'

 L.1139       534  LOAD_GLOBAL              util
              536  LOAD_METHOD              lower
              538  LOAD_FAST                'k'
              540  CALL_METHOD_1         1  '1 positional argument'
              542  LOAD_STR                 'content'
              544  COMPARE_OP               ==
          546_548  POP_JUMP_IF_FALSE   554  'to 554'

 L.1140       550  LOAD_FAST                'v'
              552  STORE_FAST               'content'
            554_0  COME_FROM           546  '546'

 L.1141       554  LOAD_FAST                'c_lang'
          556_558  POP_JUMP_IF_FALSE_BACK   490  'to 490'
              560  LOAD_FAST                'content'
          562_564  POP_JUMP_IF_FALSE_BACK   490  'to 490'

 L.1142       566  LOAD_FAST                'content'
              568  STORE_FAST               'found_lang'

 L.1143       570  LOAD_FAST                'self'
              572  LOAD_ATTR                cached_meta_lang
              574  LOAD_METHOD              append
              576  LOAD_FAST                'root'
              578  LOAD_FAST                'found_lang'
              580  BUILD_TUPLE_2         2 
              582  CALL_METHOD_1         1  '1 positional argument'
              584  POP_TOP          

 L.1144       586  BREAK_LOOP       
          588_590  JUMP_BACK           490  'to 490'
              592  POP_BLOCK        
            594_0  COME_FROM_LOOP      478  '478'
            594_1  COME_FROM           466  '466'
            594_2  COME_FROM           454  '454'
            594_3  COME_FROM           438  '438'

 L.1145       594  LOAD_FAST                'found_lang'
          596_598  POP_JUMP_IF_FALSE_BACK   426  'to 426'

 L.1146       600  BREAK_LOOP       
          602_604  JUMP_BACK           426  'to 426'
              606  POP_BLOCK        
            608_0  COME_FROM_LOOP      420  '420'

 L.1147       608  LOAD_FAST                'found_lang'
          610_612  POP_JUMP_IF_TRUE    630  'to 630'

 L.1148       614  LOAD_FAST                'self'
              616  LOAD_ATTR                cached_meta_lang
              618  LOAD_METHOD              append
              620  LOAD_FAST                'root'
              622  LOAD_CONST               False
              624  BUILD_TUPLE_2         2 
              626  CALL_METHOD_1         1  '1 positional argument'
              628  POP_TOP          
            630_0  COME_FROM           610  '610'
            630_1  COME_FROM           416  '416'
            630_2  COME_FROM           312  '312'
            630_3  COME_FROM           300  '300'
            630_4  COME_FROM           286  '286'

 L.1151       630  LOAD_FAST                'found_lang'
          632_634  POP_JUMP_IF_FALSE   698  'to 698'

 L.1152       636  SETUP_LOOP          698  'to 698'
              638  LOAD_FAST                'langs'
              640  GET_ITER         
            642_0  COME_FROM           692  '692'
            642_1  COME_FROM           686  '686'
              642  FOR_ITER            696  'to 696'
              644  STORE_FAST               'patterns'

 L.1153       646  LOAD_CONST               False
              648  STORE_FAST               'match'

 L.1154       650  SETUP_LOOP          684  'to 684'
              652  LOAD_FAST                'patterns'
              654  GET_ITER         
            656_0  COME_FROM           678  '678'
            656_1  COME_FROM           670  '670'
              656  FOR_ITER            682  'to 682'
              658  STORE_FAST               'pattern'

 L.1155       660  LOAD_FAST                'self'
              662  LOAD_METHOD              extended_language_filter
              664  LOAD_FAST                'pattern'
              666  LOAD_FAST                'found_lang'
              668  CALL_METHOD_2         2  '2 positional arguments'
          670_672  POP_JUMP_IF_FALSE_BACK   656  'to 656'

 L.1156       674  LOAD_CONST               True
              676  STORE_FAST               'match'
          678_680  JUMP_BACK           656  'to 656'
              682  POP_BLOCK        
            684_0  COME_FROM_LOOP      650  '650'

 L.1157       684  LOAD_FAST                'match'
          686_688  POP_JUMP_IF_TRUE_BACK   642  'to 642'

 L.1158       690  BREAK_LOOP       
          692_694  JUMP_BACK           642  'to 642'
              696  POP_BLOCK        
            698_0  COME_FROM_LOOP      636  '636'
            698_1  COME_FROM           632  '632'

 L.1160       698  LOAD_FAST                'match'
              700  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 178_0

    def match_dir(self, el, directionality):
        """Check directionality."""
        if directionality & ct.SEL_DIR_LTR:
            if directionality & ct.SEL_DIR_RTL:
                return False
        if not (el is None or self.is_html_tag(el)):
            return False
        direction = DIR_MAP.get(util.lower(self.get_attribute_by_name(el, 'dir', '')), None)
        if direction not in (None, 0):
            return direction == directionality
        is_root = self.is_root(el)
        if is_root:
            if direction is None:
                return ct.SEL_DIR_LTR == directionality
        name = self.get_tag(el)
        is_input = name == 'input'
        is_textarea = name == 'textarea'
        is_bdi = name == 'bdi'
        itype = util.lower(self.get_attribute_by_name(el, 'type', '')) if is_input else ''
        if is_input:
            if itype == 'tel':
                if direction is None:
                    return ct.SEL_DIR_LTR == directionality
        if is_input and itype in ('text', 'search', 'tel', 'url', 'email') or is_textarea:
            if direction == 0:
                if is_textarea:
                    value = []
                    for node in self.get_contents(el, no_iframe=True):
                        if self.is_content_string(node):
                            value.append(node)

                    value = ''.join(value)
                else:
                    value = self.get_attribute_by_name(el, 'value', '')
                if value:
                    for c in value:
                        bidi = unicodedata.bidirectional(c)
                        if bidi in ('AL', 'R', 'L'):
                            direction = ct.SEL_DIR_LTR if bidi == 'L' else ct.SEL_DIR_RTL
                            return direction == directionality

                    return ct.SEL_DIR_LTR == directionality
                if is_root:
                    return ct.SEL_DIR_LTR == directionality
                return self.match_dir(self.get_parent(el, no_iframe=True), directionality)
        if is_bdi and direction is None or direction == 0:
            direction = self.find_bidi(el)
            if direction is not None:
                return direction == directionality
            if is_root:
                return ct.SEL_DIR_LTR == directionality
            return self.match_dir(self.get_parent(el, no_iframe=True), directionality)
        return self.match_dir(self.get_parent(el, no_iframe=True), directionality)

    def match_range(self, el, condition):
        """
        Match range.

        Behavior is modeled after what we see in browsers. Browsers seem to evaluate
        if the value is out of range, and if not, it is in range. So a missing value
        will not evaluate out of range; therefore, value is in range. Personally, I
        feel like this should evaluate as neither in or out of range.
        """
        out_of_range = False
        itype = util.lower(self.get_attribute_by_name(el, 'type'))
        mn = self.get_attribute_by_name(el, 'min', None)
        if mn is not None:
            mn = Inputs.parse_value(itype, mn)
        mx = self.get_attribute_by_name(el, 'max', None)
        if mx is not None:
            mx = Inputs.parse_value(itype, mx)
        if mn is None:
            if mx is None:
                return False
        value = self.get_attribute_by_name(el, 'value', None)
        if value is not None:
            value = Inputs.parse_value(itype, value)
        if value is not None:
            if itype in ('date', 'datetime-local', 'month', 'week', 'number', 'range'):
                if mn is not None:
                    if value < mn:
                        out_of_range = True
                if not out_of_range:
                    if mx is not None:
                        if value > mx:
                            out_of_range = True
            else:
                pass
            if itype == 'time':
                if mn is not None and mx is not None and mn > mx:
                    if not value < mn or value > mx:
                        out_of_range = True
                else:
                    if mn is not None:
                        if value < mn:
                            out_of_range = True
                    if not out_of_range:
                        if mx is not None:
                            if value > mx:
                                out_of_range = True
                if condition & ct.SEL_IN_RANGE:
                    return not out_of_range
            return out_of_range

    def match_defined(self, el):
        """
        Match defined.

        `:defined` is related to custom elements in a browser.

        - If the document is XML (not XHTML), all tags will match.
        - Tags that are not custom (don't have a hyphen) are marked defined.
        - If the tag has a prefix (without or without a namespace), it will not match.

        This is of course requires the parser to provide us with the proper prefix and namespace info,
        if it doesn't, there is nothing we can do.
        """
        name = self.get_tag(el)
        return name.find('-') == -1 or name.find(':') != -1 or self.get_prefix(el) is not None

    def match_placeholder_shown(self, el):
        """
        Match placeholder shown according to HTML spec.

        - text area should be checked if they have content. A single newline does not count as content.

        """
        match = False
        content = self.get_text(el)
        if content in ('', '\n'):
            match = True
        return match

    def match_selectors(self, el, selectors):
        """Check if element matches one of the selectors."""
        match = False
        is_not = selectors.is_not
        is_html = selectors.is_html
        if is_html:
            namespaces = self.namespaces
            iframe_restrict = self.iframe_restrict
            self.namespaces = {'html': NS_XHTML}
            self.iframe_restrict = True
        if not is_html or self.is_html:
            for selector in selectors:
                match = is_not
                if isinstance(selector, ct.SelectorNull):
                    continue
                if not self.match_tag(el, selector.tag):
                    continue
                if selector.flags & ct.SEL_DEFINED:
                    if not self.match_defined(el):
                        continue
                    if selector.flags & ct.SEL_ROOT:
                        if not self.match_root(el):
                            continue
                        if selector.flags & ct.SEL_SCOPE:
                            if not self.match_scope(el):
                                continue
                            if selector.flags & ct.SEL_PLACEHOLDER_SHOWN:
                                if not self.match_placeholder_shown(el):
                                    continue
                                if not self.match_nth(el, selector.nth):
                                    continue
                                if selector.flags & ct.SEL_EMPTY:
                                    if not self.match_empty(el):
                                        continue
                                    if selector.ids:
                                        if not self.match_id(el, selector.ids):
                                            continue
                                        if selector.classes:
                                            if not self.match_classes(el, selector.classes):
                                                continue
                                            if not self.match_attributes(el, selector.attributes):
                                                continue
                                            if selector.flags & RANGES:
                                                if not self.match_range(el, selector.flags & RANGES):
                                                    continue
                                                if selector.lang:
                                                    if not self.match_lang(el, selector.lang):
                                                        continue
                                                    if selector.selectors:
                                                        if not self.match_subselectors(el, selector.selectors):
                                                            continue
                                                        if selector.relation:
                                                            if not self.match_relations(el, selector.relation):
                                                                continue
                                                            if selector.flags & ct.SEL_DEFAULT:
                                                                if not self.match_default(el):
                                                                    continue
                                                                if selector.flags & ct.SEL_INDETERMINATE:
                                                                    if not self.match_indeterminate(el):
                                                                        continue
                                                                    if selector.flags & DIR_FLAGS:
                                                                        if not self.match_dir(el, selector.flags & DIR_FLAGS):
                                                                            continue
                                                                        if not self.match_contains(el, selector.contains):
                                                                            continue
                                                                        else:
                                                                            match = not is_not
                                                                        break

        if is_html:
            self.namespaces = namespaces
            self.iframe_restrict = iframe_restrict
        return match

    def select(self, limit=0):
        """Match all tags under the targeted tag."""
        if limit < 1:
            limit = None
        for child in self.get_descendants(self.tag):
            if self.match(child):
                yield child
                if limit is not None:
                    limit -= 1
                    if limit < 1:
                        break

    def closest(self):
        """Match closest ancestor."""
        current = self.tag
        closest = None
        while closest is None:
            if current is not None:
                if self.match(current):
                    closest = current
                else:
                    current = self.get_parent(current)

        return closest

    def filter(self):
        """Filter tag's children."""
        return [tag for tag in self.get_contents(self.tag) if not self.is_navigable_string(tag) if self.match(tag)]

    def match(self, el):
        """Match."""
        return not self.is_doc(el) and self.is_tag(el) and self.match_selectors(el, self.selectors)


class CSSMatch(_DocumentNav, _Match):
    __doc__ = 'The Beautiful Soup CSS match class.'


class CommentsMatch(_DocumentNav):
    __doc__ = 'Comments matcher.'

    def __init__(self, el):
        """Initialize."""
        self.assert_valid_input(el)
        self.tag = el

    def get_comments(self, limit=0):
        """Get comments."""
        if limit < 1:
            limit = None
        for child in self.get_descendants((self.tag), tags=False):
            if self.is_comment(child):
                yield child
                if limit is not None:
                    limit -= 1
                    if limit < 1:
                        break


class SoupSieve(ct.Immutable):
    __doc__ = 'Compiled Soup Sieve selector matching object.'
    __slots__ = ('pattern', 'selectors', 'namespaces', 'custom', 'flags', '_hash')

    def __init__(self, pattern, selectors, namespaces, custom, flags):
        super(SoupSieve, self).__init__(pattern=pattern,
          selectors=selectors,
          namespaces=namespaces,
          custom=custom,
          flags=flags)

    def match(self, tag):
        """Match."""
        return CSSMatch(self.selectors, tag, self.namespaces, self.flags).match(tag)

    def closest(self, tag):
        """Match closest ancestor."""
        return CSSMatch(self.selectors, tag, self.namespaces, self.flags).closest()

    def filter(self, iterable):
        """
        Filter.

        `CSSMatch` can cache certain searches for tags of the same document,
        so if we are given a tag, all tags are from the same document,
        and we can take advantage of the optimization.

        Any other kind of iterable could have tags from different documents or detached tags,
        so for those, we use a new `CSSMatch` for each item in the iterable.
        """
        if CSSMatch.is_tag(iterable):
            return CSSMatch(self.selectors, iterable, self.namespaces, self.flags).filter()
        return [node for node in iterable if not CSSMatch.is_navigable_string(node) if self.match(node)]

    @util.deprecated("'comments' is not related to CSS selectors and will be removed in the future.")
    def comments(self, tag, limit=0):
        """Get comments only."""
        return [comment for comment in CommentsMatch(tag).get_comments(limit)]

    @util.deprecated("'icomments' is not related to CSS selectors and will be removed in the future.")
    def icomments(self, tag, limit=0):
        """Iterate comments only."""
        for comment in CommentsMatch(tag).get_comments(limit):
            yield comment

    def select_one(self, tag):
        """Select a single tag."""
        tags = self.select(tag, limit=1)
        if tags:
            return tags[0]

    def select(self, tag, limit=0):
        """Select the specified tags."""
        return list(self.iselect(tag, limit))

    def iselect(self, tag, limit=0):
        """Iterate the specified tags."""
        for el in CSSMatch(self.selectors, tag, self.namespaces, self.flags).select(limit):
            yield el

    def __repr__(self):
        """Representation."""
        return 'SoupSieve(pattern={!r}, namespaces={!r}, custom={!r}, flags={!r})'.format(self.pattern, self.namespaces, self.custom, self.flags)

    __str__ = __repr__


ct.pickle_register(SoupSieve)