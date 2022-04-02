# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
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

else:

    class HTML5TreeBuilder(HTMLTreeBuilder):
        __doc__ = "Use html5lib to build a tree.\n\n    Note that this TreeBuilder does not support some features common\n    to HTML TreeBuilders. Some of these features could theoretically\n    be implemented, but at the very least it's quite difficult,\n    because html5lib moves the parse tree around as it's being built.\n\n    * This TreeBuilder doesn't use different subclasses of NavigableString\n      based on the name of the tag in which the string was found.\n\n    * You can't use a SoupStrainer to parse only part of a document.\n    "
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

 L. 192         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'element'
                4  LOAD_DEREF               'BeautifulSoup'
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    10  'to 10'
             10_0  COME_FROM             8  '8'

 L. 194        10  LOAD_GLOBAL              isinstance
               12  LOAD_FAST                'element'
               14  LOAD_GLOBAL              Doctype
               16  CALL_FUNCTION_2       2  ''
               18  POP_JUMP_IF_FALSE   168  'to 168'

 L. 195        20  LOAD_DEREF               'doctype_re'
               22  LOAD_METHOD              match
               24  LOAD_FAST                'element'
               26  CALL_METHOD_1         1  ''
               28  STORE_FAST               'm'

 L. 196        30  LOAD_FAST                'm'
               32  POP_JUMP_IF_FALSE   144  'to 144'

 L. 197        34  LOAD_FAST                'm'
               36  LOAD_METHOD              group
               38  LOAD_CONST               1
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'name'

 L. 198        44  LOAD_FAST                'm'
               46  LOAD_ATTR                lastindex
               48  LOAD_CONST               1
               50  COMPARE_OP               >
               52  POP_JUMP_IF_FALSE   120  'to 120'

 L. 199        54  LOAD_FAST                'm'
               56  LOAD_METHOD              group
               58  LOAD_CONST               2
               60  CALL_METHOD_1         1  ''
               62  JUMP_IF_TRUE_OR_POP    66  'to 66'
               64  LOAD_STR                 ''
             66_0  COME_FROM            62  '62'
               66  STORE_FAST               'publicId'

 L. 200        68  LOAD_FAST                'm'
               70  LOAD_METHOD              group
               72  LOAD_CONST               3
               74  CALL_METHOD_1         1  ''
               76  JUMP_IF_TRUE_OR_POP    90  'to 90'
               78  LOAD_FAST                'm'
               80  LOAD_METHOD              group
               82  LOAD_CONST               4
               84  CALL_METHOD_1         1  ''
               86  JUMP_IF_TRUE_OR_POP    90  'to 90'
               88  LOAD_STR                 ''
             90_0  COME_FROM            86  '86'
             90_1  COME_FROM            76  '76'
               90  STORE_FAST               'systemId'

 L. 201        92  LOAD_DEREF               'rv'
               94  LOAD_METHOD              append
               96  LOAD_STR                 '|%s<!DOCTYPE %s "%s" "%s">'

 L. 202        98  LOAD_STR                 ' '
              100  LOAD_FAST                'indent'
              102  BINARY_MULTIPLY  
              104  LOAD_FAST                'name'
              106  LOAD_FAST                'publicId'
              108  LOAD_FAST                'systemId'
              110  BUILD_TUPLE_4         4 

 L. 201       112  BINARY_MODULO    
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          
              118  JUMP_ABSOLUTE       164  'to 164'
            120_0  COME_FROM            52  '52'

 L. 204       120  LOAD_DEREF               'rv'
              122  LOAD_METHOD              append
              124  LOAD_STR                 '|%s<!DOCTYPE %s>'
              126  LOAD_STR                 ' '
              128  LOAD_FAST                'indent'
              130  BINARY_MULTIPLY  
              132  LOAD_FAST                'name'
              134  BUILD_TUPLE_2         2 
              136  BINARY_MODULO    
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
              142  JUMP_FORWARD        482  'to 482'
            144_0  COME_FROM            32  '32'

 L. 206       144  LOAD_DEREF               'rv'
              146  LOAD_METHOD              append
              148  LOAD_STR                 '|%s<!DOCTYPE >'
              150  LOAD_STR                 ' '
              152  LOAD_FAST                'indent'
              154  BINARY_MULTIPLY  
              156  BUILD_TUPLE_1         1 
              158  BINARY_MODULO    
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          
          164_166  JUMP_FORWARD        482  'to 482'
            168_0  COME_FROM            18  '18'

 L. 207       168  LOAD_GLOBAL              isinstance
              170  LOAD_FAST                'element'
              172  LOAD_GLOBAL              Comment
              174  CALL_FUNCTION_2       2  ''
              176  POP_JUMP_IF_FALSE   204  'to 204'

 L. 208       178  LOAD_DEREF               'rv'
              180  LOAD_METHOD              append
              182  LOAD_STR                 '|%s<!-- %s -->'
              184  LOAD_STR                 ' '
              186  LOAD_FAST                'indent'
              188  BINARY_MULTIPLY  
              190  LOAD_FAST                'element'
              192  BUILD_TUPLE_2         2 
              194  BINARY_MODULO    
              196  CALL_METHOD_1         1  ''
              198  POP_TOP          
          200_202  JUMP_FORWARD        482  'to 482'
            204_0  COME_FROM           176  '176'

 L. 209       204  LOAD_GLOBAL              isinstance
              206  LOAD_FAST                'element'
              208  LOAD_GLOBAL              NavigableString
              210  CALL_FUNCTION_2       2  ''
              212  POP_JUMP_IF_FALSE   238  'to 238'

 L. 210       214  LOAD_DEREF               'rv'
              216  LOAD_METHOD              append
              218  LOAD_STR                 '|%s"%s"'
              220  LOAD_STR                 ' '
              222  LOAD_FAST                'indent'
              224  BINARY_MULTIPLY  
              226  LOAD_FAST                'element'
              228  BUILD_TUPLE_2         2 
              230  BINARY_MODULO    
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          
              236  JUMP_FORWARD        482  'to 482'
            238_0  COME_FROM           212  '212'

 L. 212       238  LOAD_FAST                'element'
              240  LOAD_ATTR                namespace
          242_244  POP_JUMP_IF_FALSE   268  'to 268'

 L. 213       246  LOAD_STR                 '%s %s'
              248  LOAD_GLOBAL              prefixes
              250  LOAD_FAST                'element'
              252  LOAD_ATTR                namespace
              254  BINARY_SUBSCR    

 L. 214       256  LOAD_FAST                'element'
              258  LOAD_ATTR                name

 L. 213       260  BUILD_TUPLE_2         2 
              262  BINARY_MODULO    
              264  STORE_FAST               'name'
              266  JUMP_FORWARD        274  'to 274'
            268_0  COME_FROM           242  '242'

 L. 216       268  LOAD_FAST                'element'
              270  LOAD_ATTR                name
              272  STORE_FAST               'name'
            274_0  COME_FROM           266  '266'

 L. 217       274  LOAD_DEREF               'rv'
              276  LOAD_METHOD              append
              278  LOAD_STR                 '|%s<%s>'
              280  LOAD_STR                 ' '
              282  LOAD_FAST                'indent'
              284  BINARY_MULTIPLY  
              286  LOAD_FAST                'name'
              288  BUILD_TUPLE_2         2 
              290  BINARY_MODULO    
              292  CALL_METHOD_1         1  ''
              294  POP_TOP          

 L. 218       296  LOAD_FAST                'element'
              298  LOAD_ATTR                attrs
          300_302  POP_JUMP_IF_FALSE   450  'to 450'

 L. 219       304  BUILD_LIST_0          0 
              306  STORE_FAST               'attributes'

 L. 220       308  LOAD_GLOBAL              list
              310  LOAD_FAST                'element'
              312  LOAD_ATTR                attrs
              314  LOAD_METHOD              items
              316  CALL_METHOD_0         0  ''
              318  CALL_FUNCTION_1       1  ''
              320  GET_ITER         
              322  FOR_ITER            402  'to 402'
              324  UNPACK_SEQUENCE_2     2 
              326  STORE_FAST               'name'
              328  STORE_FAST               'value'

 L. 221       330  LOAD_GLOBAL              isinstance
              332  LOAD_FAST                'name'
              334  LOAD_GLOBAL              NamespacedAttribute
              336  CALL_FUNCTION_2       2  ''
          338_340  POP_JUMP_IF_FALSE   362  'to 362'

 L. 222       342  LOAD_STR                 '%s %s'
              344  LOAD_GLOBAL              prefixes
              346  LOAD_FAST                'name'
              348  LOAD_ATTR                namespace
              350  BINARY_SUBSCR    
              352  LOAD_FAST                'name'
              354  LOAD_ATTR                name
              356  BUILD_TUPLE_2         2 
              358  BINARY_MODULO    
              360  STORE_FAST               'name'
            362_0  COME_FROM           338  '338'

 L. 223       362  LOAD_GLOBAL              isinstance
              364  LOAD_FAST                'value'
              366  LOAD_GLOBAL              list
              368  CALL_FUNCTION_2       2  ''
          370_372  POP_JUMP_IF_FALSE   384  'to 384'

 L. 224       374  LOAD_STR                 ' '
              376  LOAD_METHOD              join
              378  LOAD_FAST                'value'
              380  CALL_METHOD_1         1  ''
              382  STORE_FAST               'value'
            384_0  COME_FROM           370  '370'

 L. 225       384  LOAD_FAST                'attributes'
              386  LOAD_METHOD              append
              388  LOAD_FAST                'name'
              390  LOAD_FAST                'value'
              392  BUILD_TUPLE_2         2 
              394  CALL_METHOD_1         1  ''
              396  POP_TOP          
          398_400  JUMP_BACK           322  'to 322'

 L. 227       402  LOAD_GLOBAL              sorted
              404  LOAD_FAST                'attributes'
              406  CALL_FUNCTION_1       1  ''
              408  GET_ITER         
              410  FOR_ITER            450  'to 450'
              412  UNPACK_SEQUENCE_2     2 
              414  STORE_FAST               'name'
              416  STORE_FAST               'value'

 L. 228       418  LOAD_DEREF               'rv'
              420  LOAD_METHOD              append
              422  LOAD_STR                 '|%s%s="%s"'
              424  LOAD_STR                 ' '
              426  LOAD_FAST                'indent'
              428  LOAD_CONST               2
              430  BINARY_ADD       
              432  BINARY_MULTIPLY  
              434  LOAD_FAST                'name'
              436  LOAD_FAST                'value'
              438  BUILD_TUPLE_3         3 
              440  BINARY_MODULO    
              442  CALL_METHOD_1         1  ''
              444  POP_TOP          
          446_448  JUMP_BACK           410  'to 410'
            450_0  COME_FROM           300  '300'

 L. 229       450  LOAD_FAST                'indent'
              452  LOAD_CONST               2
              454  INPLACE_ADD      
              456  STORE_FAST               'indent'
            458_0  COME_FROM           142  '142'

 L. 230       458  LOAD_FAST                'element'
              460  LOAD_ATTR                children
              462  GET_ITER         
              464  FOR_ITER            482  'to 482'
              466  STORE_FAST               'child'

 L. 231       468  LOAD_DEREF               'serializeElement'
              470  LOAD_FAST                'child'
              472  LOAD_FAST                'indent'
              474  CALL_FUNCTION_2       2  ''
              476  POP_TOP          
          478_480  JUMP_BACK           464  'to 464'
            482_0  COME_FROM           236  '236'
            482_1  COME_FROM           200  '200'
            482_2  COME_FROM           164  '164'

Parse error at or near `COME_FROM' instruction at offset 482_1

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
                    else:
                        self.soup.builder._replace_cdata_list_attribute_values(self.name, attributes)
                        for name, value in list(attributes.items()):
                            self.element[name] = value
                        else:
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
            else:
                element.contents = []
                element.next_element = final_next_element

        def cloneNode(self):
            tag = self.soup.new_tag(self.element.name, self.namespace)
            node = Element(tag, self.soup, self.namespace)
            for key, value in self.attributes:
                node.attributes[key] = value
            else:
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