# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\bs4\builder\_html5lib.py
__license__ = 'MIT'
__all__ = [
 'HTML5TreeBuilder']
import warnings, re
from bs4.builder import PERMISSIVE, HTML, HTML_5, HTMLTreeBuilder
from bs4.element import NamespacedAttribute, nonwhitespace_re
import html5lib
from html5lib.constants import namespaces, prefixes
from bs4.element import Comment, Doctype, NavigableString, Tag
try:
    import html5lib.treebuilders as treebuilder_base
    new_html5lib = False
except ImportError as e:
    try:
        import html5lib.treebuilders as treebuilder_base
        new_html5lib = True
    finally:
        e = None
        del e

class HTML5TreeBuilder(HTMLTreeBuilder):
    __doc__ = 'Use html5lib to build a tree.'
    NAME = 'html5lib'
    features = [
     NAME, PERMISSIVE, HTML_5, HTML]
    TRACKS_LINE_NUMBERS = True

    def prepare_markup(self, markup, user_specified_encoding, document_declared_encoding=None, exclude_encodings=None):
        self.user_specified_encoding = user_specified_encoding
        if exclude_encodings:
            warnings.warn("You provided a value for exclude_encoding, but the html5lib tree builder doesn't support exclude_encoding.")
        yield (
         markup, None, None, False)

    def feed(self, markup):
        if self.soup.parse_only is not None:
            warnings.warn("You provided a value for parse_only, but the html5lib tree builder doesn't support parse_only. The entire document will be parsed.")
        else:
            parser = html5lib.HTMLParser(tree=(self.create_treebuilder))
            self.underlying_builder.parser = parser
            extra_kwargs = dict()
            if not isinstance(markup, str):
                if new_html5lib:
                    extra_kwargs['override_encoding'] = self.user_specified_encoding
                else:
                    extra_kwargs['encoding'] = self.user_specified_encoding
        doc = (parser.parse)(markup, **extra_kwargs)
        if isinstance(markup, str):
            doc.original_encoding = None
        else:
            original_encoding = parser.tokenizer.stream.charEncoding[0]
            if not isinstance(original_encoding, str):
                original_encoding = original_encoding.name
            doc.original_encoding = original_encoding
        self.underlying_builder.parser = None

    def create_treebuilder(self, namespaceHTMLElements):
        self.underlying_builder = TreeBuilderForHtml5lib(namespaceHTMLElements,
          (self.soup), store_line_numbers=(self.store_line_numbers))
        return self.underlying_builder

    def test_fragment_to_document(self, fragment):
        """See `TreeBuilder`."""
        return '<html><head></head><body>%s</body></html>' % fragment


class TreeBuilderForHtml5lib(treebuilder_base.TreeBuilder):

    def __init__(self, namespaceHTMLElements, soup=None, store_line_numbers=True, **kwargs):
        if soup:
            self.soup = soup
        else:
            from bs4 import BeautifulSoup
            self.soup = BeautifulSoup('', 'html.parser', store_line_numbers=store_line_numbers, **kwargs)
        super(TreeBuilderForHtml5lib, self).__init__(namespaceHTMLElements)
        self.parser = None
        self.store_line_numbers = store_line_numbers

    def documentClass(self):
        self.soup.reset()
        return Element(self.soup, self.soup, None)

    def insertDoctype(self, token):
        name = token['name']
        publicId = token['publicId']
        systemId = token['systemId']
        doctype = Doctype.for_name_and_ids(name, publicId, systemId)
        self.soup.object_was_parsed(doctype)

    def elementClass(self, name, namespace):
        kwargs = {}
        if self.parser:
            if self.store_line_numbers:
                sourceline, sourcepos = self.parser.tokenizer.stream.position()
                kwargs['sourceline'] = sourceline
                kwargs['sourcepos'] = sourcepos - 1
        tag = (self.soup.new_tag)(name, namespace, **kwargs)
        return Element(tag, self.soup, namespace)

    def commentClass(self, data):
        return TextNode(Comment(data), self.soup)

    def fragmentClass(self):
        from bs4 import BeautifulSoup
        self.soup = BeautifulSoup('', 'html.parser')
        self.soup.name = '[document_fragment]'
        return Element(self.soup, self.soup, None)

    def appendChild(self, node):
        self.soup.append(node.element)

    def getDocument(self):
        return self.soup

    def getFragment(self):
        return treebuilder_base.TreeBuilder.getFragment(self).element

    def testSerializer(self, element):
        from bs4 import BeautifulSoup
        rv = []
        doctype_re = re.compile('^(.*?)(?: PUBLIC "(.*?)"(?: "(.*?)")?| SYSTEM "(.*?)")?$')

        def serializeElement--- This code section failed: ---

 L. 178         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'element'
                4  LOAD_DEREF               'BeautifulSoup'
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_FALSE    10  'to 10'
             10_0  COME_FROM             8  '8'

 L. 180        10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'element'
               14  LOAD_GLOBAL              Doctype
               16  CALL_FUNCTION_2       2  '2 positional arguments'
               18  POP_JUMP_IF_FALSE   168  'to 168'

 L. 181        20  LOAD_DEREF               'doctype_re'
               22  LOAD_METHOD              match
               24  LOAD_FAST                'element'
               26  CALL_METHOD_1         1  '1 positional argument'
               28  STORE_FAST               'm'

 L. 182        30  LOAD_FAST                'm'
               32  POP_JUMP_IF_FALSE   144  'to 144'

 L. 183        34  LOAD_FAST                'm'
               36  LOAD_METHOD              group
               38  LOAD_CONST               1
               40  CALL_METHOD_1         1  '1 positional argument'
               42  STORE_FAST               'name'

 L. 184        44  LOAD_FAST                'm'
               46  LOAD_ATTR                lastindex
               48  LOAD_CONST               1
               50  COMPARE_OP               >
               52  POP_JUMP_IF_FALSE   120  'to 120'

 L. 185        54  LOAD_FAST                'm'
               56  LOAD_METHOD              group
               58  LOAD_CONST               2
               60  CALL_METHOD_1         1  '1 positional argument'
               62  JUMP_IF_TRUE_OR_POP    66  'to 66'
               64  LOAD_STR                 ''
             66_0  COME_FROM            62  '62'
               66  STORE_FAST               'publicId'

 L. 186        68  LOAD_FAST                'm'
               70  LOAD_METHOD              group
               72  LOAD_CONST               3
               74  CALL_METHOD_1         1  '1 positional argument'
               76  JUMP_IF_TRUE_OR_POP    90  'to 90'
               78  LOAD_FAST                'm'
               80  LOAD_METHOD              group
               82  LOAD_CONST               4
               84  CALL_METHOD_1         1  '1 positional argument'
               86  JUMP_IF_TRUE_OR_POP    90  'to 90'
               88  LOAD_STR                 ''
             90_0  COME_FROM            86  '86'
             90_1  COME_FROM            76  '76'
               90  STORE_FAST               'systemId'

 L. 187        92  LOAD_DEREF               'rv'
               94  LOAD_METHOD              append
               96  LOAD_STR                 '|%s<!DOCTYPE %s "%s" "%s">'

 L. 188        98  LOAD_STR                 ' '
              100  LOAD_FAST                'indent'
              102  BINARY_MULTIPLY  
              104  LOAD_FAST                'name'
              106  LOAD_FAST                'publicId'
              108  LOAD_FAST                'systemId'
              110  BUILD_TUPLE_4         4 
              112  BINARY_MODULO    
              114  CALL_METHOD_1         1  '1 positional argument'
              116  POP_TOP          
              118  JUMP_ABSOLUTE       164  'to 164'
            120_0  COME_FROM            52  '52'

 L. 190       120  LOAD_DEREF               'rv'
              122  LOAD_METHOD              append
              124  LOAD_STR                 '|%s<!DOCTYPE %s>'
              126  LOAD_STR                 ' '
              128  LOAD_FAST                'indent'
              130  BINARY_MULTIPLY  
              132  LOAD_FAST                'name'
              134  BUILD_TUPLE_2         2 
              136  BINARY_MODULO    
              138  CALL_METHOD_1         1  '1 positional argument'
              140  POP_TOP          
              142  JUMP_FORWARD        496  'to 496'
            144_0  COME_FROM            32  '32'

 L. 192       144  LOAD_DEREF               'rv'
              146  LOAD_METHOD              append
              148  LOAD_STR                 '|%s<!DOCTYPE >'
              150  LOAD_STR                 ' '
              152  LOAD_FAST                'indent'
              154  BINARY_MULTIPLY  
              156  BUILD_TUPLE_1         1 
              158  BINARY_MODULO    
              160  CALL_METHOD_1         1  '1 positional argument'
              162  POP_TOP          
          164_166  JUMP_FORWARD        496  'to 496'
            168_0  COME_FROM            18  '18'

 L. 193       168  LOAD_GLOBAL              isinstance
              170  LOAD_FAST                'element'
              172  LOAD_GLOBAL              Comment
              174  CALL_FUNCTION_2       2  '2 positional arguments'
              176  POP_JUMP_IF_FALSE   204  'to 204'

 L. 194       178  LOAD_DEREF               'rv'
              180  LOAD_METHOD              append
              182  LOAD_STR                 '|%s<!-- %s -->'
              184  LOAD_STR                 ' '
              186  LOAD_FAST                'indent'
              188  BINARY_MULTIPLY  
              190  LOAD_FAST                'element'
              192  BUILD_TUPLE_2         2 
              194  BINARY_MODULO    
              196  CALL_METHOD_1         1  '1 positional argument'
              198  POP_TOP          
          200_202  JUMP_FORWARD        496  'to 496'
            204_0  COME_FROM           176  '176'

 L. 195       204  LOAD_GLOBAL              isinstance
              206  LOAD_FAST                'element'
              208  LOAD_GLOBAL              NavigableString
              210  CALL_FUNCTION_2       2  '2 positional arguments'
              212  POP_JUMP_IF_FALSE   240  'to 240'

 L. 196       214  LOAD_DEREF               'rv'
              216  LOAD_METHOD              append
              218  LOAD_STR                 '|%s"%s"'
              220  LOAD_STR                 ' '
              222  LOAD_FAST                'indent'
              224  BINARY_MULTIPLY  
              226  LOAD_FAST                'element'
              228  BUILD_TUPLE_2         2 
              230  BINARY_MODULO    
              232  CALL_METHOD_1         1  '1 positional argument'
              234  POP_TOP          
          236_238  JUMP_FORWARD        496  'to 496'
            240_0  COME_FROM           212  '212'

 L. 198       240  LOAD_FAST                'element'
              242  LOAD_ATTR                namespace
          244_246  POP_JUMP_IF_FALSE   270  'to 270'

 L. 199       248  LOAD_STR                 '%s %s'
              250  LOAD_GLOBAL              prefixes
              252  LOAD_FAST                'element'
              254  LOAD_ATTR                namespace
              256  BINARY_SUBSCR    

 L. 200       258  LOAD_FAST                'element'
              260  LOAD_ATTR                name
              262  BUILD_TUPLE_2         2 
              264  BINARY_MODULO    
              266  STORE_FAST               'name'
              268  JUMP_FORWARD        276  'to 276'
            270_0  COME_FROM           244  '244'

 L. 202       270  LOAD_FAST                'element'
              272  LOAD_ATTR                name
              274  STORE_FAST               'name'
            276_0  COME_FROM           268  '268'

 L. 203       276  LOAD_DEREF               'rv'
              278  LOAD_METHOD              append
              280  LOAD_STR                 '|%s<%s>'
              282  LOAD_STR                 ' '
              284  LOAD_FAST                'indent'
              286  BINARY_MULTIPLY  
              288  LOAD_FAST                'name'
              290  BUILD_TUPLE_2         2 
              292  BINARY_MODULO    
              294  CALL_METHOD_1         1  '1 positional argument'
              296  POP_TOP          

 L. 204       298  LOAD_FAST                'element'
              300  LOAD_ATTR                attrs
          302_304  POP_JUMP_IF_FALSE   460  'to 460'

 L. 205       306  BUILD_LIST_0          0 
              308  STORE_FAST               'attributes'

 L. 206       310  SETUP_LOOP          408  'to 408'
              312  LOAD_GLOBAL              list
              314  LOAD_FAST                'element'
              316  LOAD_ATTR                attrs
              318  LOAD_METHOD              items
              320  CALL_METHOD_0         0  '0 positional arguments'
              322  CALL_FUNCTION_1       1  '1 positional argument'
              324  GET_ITER         
              326  FOR_ITER            406  'to 406'
              328  UNPACK_SEQUENCE_2     2 
              330  STORE_FAST               'name'
              332  STORE_FAST               'value'

 L. 207       334  LOAD_GLOBAL              isinstance
              336  LOAD_FAST                'name'
              338  LOAD_GLOBAL              NamespacedAttribute
              340  CALL_FUNCTION_2       2  '2 positional arguments'
          342_344  POP_JUMP_IF_FALSE   366  'to 366'

 L. 208       346  LOAD_STR                 '%s %s'
              348  LOAD_GLOBAL              prefixes
              350  LOAD_FAST                'name'
              352  LOAD_ATTR                namespace
              354  BINARY_SUBSCR    
              356  LOAD_FAST                'name'
              358  LOAD_ATTR                name
              360  BUILD_TUPLE_2         2 
              362  BINARY_MODULO    
              364  STORE_FAST               'name'
            366_0  COME_FROM           342  '342'

 L. 209       366  LOAD_GLOBAL              isinstance
              368  LOAD_FAST                'value'
              370  LOAD_GLOBAL              list
              372  CALL_FUNCTION_2       2  '2 positional arguments'
          374_376  POP_JUMP_IF_FALSE   388  'to 388'

 L. 210       378  LOAD_STR                 ' '
              380  LOAD_METHOD              join
              382  LOAD_FAST                'value'
              384  CALL_METHOD_1         1  '1 positional argument'
              386  STORE_FAST               'value'
            388_0  COME_FROM           374  '374'

 L. 211       388  LOAD_FAST                'attributes'
              390  LOAD_METHOD              append
              392  LOAD_FAST                'name'
              394  LOAD_FAST                'value'
              396  BUILD_TUPLE_2         2 
              398  CALL_METHOD_1         1  '1 positional argument'
              400  POP_TOP          
          402_404  JUMP_BACK           326  'to 326'
              406  POP_BLOCK        
            408_0  COME_FROM_LOOP      310  '310'

 L. 213       408  SETUP_LOOP          460  'to 460'
              410  LOAD_GLOBAL              sorted
              412  LOAD_FAST                'attributes'
              414  CALL_FUNCTION_1       1  '1 positional argument'
              416  GET_ITER         
              418  FOR_ITER            458  'to 458'
              420  UNPACK_SEQUENCE_2     2 
              422  STORE_FAST               'name'
              424  STORE_FAST               'value'

 L. 214       426  LOAD_DEREF               'rv'
              428  LOAD_METHOD              append
              430  LOAD_STR                 '|%s%s="%s"'
              432  LOAD_STR                 ' '
              434  LOAD_FAST                'indent'
              436  LOAD_CONST               2
              438  BINARY_ADD       
              440  BINARY_MULTIPLY  
              442  LOAD_FAST                'name'
              444  LOAD_FAST                'value'
              446  BUILD_TUPLE_3         3 
              448  BINARY_MODULO    
              450  CALL_METHOD_1         1  '1 positional argument'
              452  POP_TOP          
          454_456  JUMP_BACK           418  'to 418'
              458  POP_BLOCK        
            460_0  COME_FROM_LOOP      408  '408'
            460_1  COME_FROM           302  '302'

 L. 215       460  LOAD_FAST                'indent'
              462  LOAD_CONST               2
              464  INPLACE_ADD      
              466  STORE_FAST               'indent'

 L. 216       468  SETUP_LOOP          496  'to 496'
              470  LOAD_FAST                'element'
            472_0  COME_FROM           142  '142'
              472  LOAD_ATTR                children
              474  GET_ITER         
              476  FOR_ITER            494  'to 494'
              478  STORE_FAST               'child'

 L. 217       480  LOAD_DEREF               'serializeElement'
              482  LOAD_FAST                'child'
              484  LOAD_FAST                'indent'
              486  CALL_FUNCTION_2       2  '2 positional arguments'
              488  POP_TOP          
          490_492  JUMP_BACK           476  'to 476'
              494  POP_BLOCK        
            496_0  COME_FROM_LOOP      468  '468'
            496_1  COME_FROM           236  '236'
            496_2  COME_FROM           200  '200'
            496_3  COME_FROM           164  '164'

Parse error at or near `LOAD_ATTR' instruction at offset 472

        serializeElement(element, 0)
        return '\n'.join(rv)


class AttrList(object):

    def __init__(self, element):
        self.element = element
        self.attrs = dict(self.element.attrs)

    def __iter__(self):
        return list(self.attrs.items()).__iter__()

    def __setitem__(self, name, value):
        list_attr = self.element.cdata_list_attributes
        if (name in list_attr['*'] or self.element.name) in list_attr:
            if name in list_attr[self.element.name]:
                if not isinstance(value, list):
                    value = nonwhitespace_re.findall(value)
        self.element[name] = value

    def items(self):
        return list(self.attrs.items())

    def keys(self):
        return list(self.attrs.keys())

    def __len__(self):
        return len(self.attrs)

    def __getitem__(self, name):
        return self.attrs[name]

    def __contains__(self, name):
        return name in list(self.attrs.keys())


class Element(treebuilder_base.Node):

    def __init__(self, element, soup, namespace):
        treebuilder_base.Node.__init__(self, element.name)
        self.element = element
        self.soup = soup
        self.namespace = namespace

    def appendChild(self, node):
        string_child = child = None
        if isinstance(node, str):
            string_child = child = node
        else:
            if isinstance(node, Tag):
                child = node
            else:
                if node.element.__class__ == NavigableString:
                    string_child = child = node.element
                    node.parent = self
                else:
                    child = node.element
                    node.parent = self
        if not isinstance(child, str):
            if child.parent is not None:
                node.element.extract()
        elif string_child is not None and self.element.contents and self.element.contents[(-1)].__class__ == NavigableString:
            old_element = self.element.contents[(-1)]
            new_element = self.soup.new_string(old_element + string_child)
            old_element.replace_with(new_element)
            self.soup._most_recent_element = new_element
        else:
            if isinstance(node, str):
                child = self.soup.new_string(node)
            elif self.element.contents:
                most_recent_element = self.element._last_descendant(False)
            else:
                if self.element.next_element is not None:
                    most_recent_element = self.soup._last_descendant()
                else:
                    most_recent_element = self.element
            self.soup.object_was_parsed(child,
              parent=(self.element), most_recent_element=most_recent_element)

    def getAttributes(self):
        if isinstance(self.element, Comment):
            return {}
        return AttrList(self.element)

    def setAttributes(self, attributes):
        if attributes is not None:
            if len(attributes) > 0:
                converted_attributes = []
                for name, value in list(attributes.items()):
                    if isinstance(name, tuple):
                        new_name = NamespacedAttribute(*name)
                        del attributes[name]
                        attributes[new_name] = value

                self.soup.builder._replace_cdata_list_attribute_values(self.name, attributes)
                for name, value in list(attributes.items()):
                    self.element[name] = value

                self.soup.builder.set_up_substitutions(self.element)

    attributes = property(getAttributes, setAttributes)

    def insertText(self, data, insertBefore=None):
        text = TextNode(self.soup.new_string(data), self.soup)
        if insertBefore:
            self.insertBefore(text, insertBefore)
        else:
            self.appendChild(text)

    def insertBefore(self, node, refNode):
        index = self.element.index(refNode.element)
        if node.element.__class__ == NavigableString and self.element.contents and self.element.contents[(index - 1)].__class__ == NavigableString:
            old_node = self.element.contents[(index - 1)]
            new_str = self.soup.new_string(old_node + node.element)
            old_node.replace_with(new_str)
        else:
            self.element.insert(index, node.element)
            node.parent = self

    def removeChild(self, node):
        node.element.extract()

    def reparentChildren(self, new_parent):
        """Move all of this tag's children into another tag."""
        element = self.element
        new_parent_element = new_parent.element
        final_next_element = element.next_sibling
        new_parents_last_descendant = new_parent_element._last_descendant(False, False)
        if len(new_parent_element.contents) > 0:
            new_parents_last_child = new_parent_element.contents[(-1)]
            new_parents_last_descendant_next_element = new_parents_last_descendant.next_element
        else:
            new_parents_last_child = None
            new_parents_last_descendant_next_element = new_parent_element.next_element
        to_append = element.contents
        if len(to_append) > 0:
            first_child = to_append[0]
            if new_parents_last_descendant is not None:
                first_child.previous_element = new_parents_last_descendant
            else:
                first_child.previous_element = new_parent_element
            first_child.previous_sibling = new_parents_last_child
            if new_parents_last_descendant is not None:
                new_parents_last_descendant.next_element = first_child
            else:
                new_parent_element.next_element = first_child
            if new_parents_last_child is not None:
                new_parents_last_child.next_sibling = first_child
            last_childs_last_descendant = to_append[(-1)]._last_descendant(False, True)
            last_childs_last_descendant.next_element = new_parents_last_descendant_next_element
            if new_parents_last_descendant_next_element is not None:
                new_parents_last_descendant_next_element.previous_element = last_childs_last_descendant
            last_childs_last_descendant.next_sibling = None
        for child in to_append:
            child.parent = new_parent_element
            new_parent_element.contents.append(child)

        element.contents = []
        element.next_element = final_next_element

    def cloneNode(self):
        tag = self.soup.new_tag(self.element.name, self.namespace)
        node = Element(tag, self.soup, self.namespace)
        for key, value in self.attributes:
            node.attributes[key] = value

        return node

    def hasContent(self):
        return self.element.contents

    def getNameTuple(self):
        if self.namespace == None:
            return (
             namespaces['html'], self.name)
        return (self.namespace, self.name)

    nameTuple = property(getNameTuple)


class TextNode(Element):

    def __init__(self, element, soup):
        treebuilder_base.Node.__init__(self, None)
        self.element = element
        self.soup = soup

    def cloneNode(self):
        raise NotImplementedError