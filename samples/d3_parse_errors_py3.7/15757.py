# decompyle3 version 3.7.5
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: gallery_dl\extractor\readcomiconline.py
"""Extractors for https://readcomiconline.to/"""
from .common import Extractor, ChapterExtractor, MangaExtractor
from .. import text, exception
import re

class ReadcomiconlineBase:
    __doc__ = 'Base class for readcomiconline extractors'
    category = 'readcomiconline'
    directory_fmt = ('{category}', '{comic}', '{issue:>03}')
    filename_fmt = '{comic}_{issue:>03}_{page:>03}.{extension}'
    archive_fmt = '{issue_id}_{page}'
    root = 'https://readcomiconline.to'

    def request--- This code section failed: ---

 L.  26         0  SETUP_LOOP          126  'to 126'
              2_0  COME_FROM           122  '122'
              2_1  COME_FROM           106  '106'

 L.  27         2  LOAD_GLOBAL              Extractor
                4  LOAD_ATTR                request
                6  LOAD_FAST                'self'
                8  LOAD_FAST                'url'
               10  BUILD_TUPLE_2         2 
               12  LOAD_FAST                'kwargs'
               14  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               16  STORE_FAST               'response'

 L.  28        18  LOAD_FAST                'response'
               20  LOAD_ATTR                history
               22  POP_JUMP_IF_FALSE    34  'to 34'
               24  LOAD_STR                 '/AreYouHuman'
               26  LOAD_FAST                'response'
               28  LOAD_ATTR                url
               30  COMPARE_OP               not-in
               32  POP_JUMP_IF_FALSE    38  'to 38'
             34_0  COME_FROM            22  '22'

 L.  29        34  LOAD_FAST                'response'
               36  RETURN_VALUE     
             38_0  COME_FROM            32  '32'

 L.  30        38  LOAD_FAST                'self'
               40  LOAD_METHOD              config
               42  LOAD_STR                 'captcha'
               44  LOAD_STR                 'stop'
               46  CALL_METHOD_2         2  '2 positional arguments'
               48  LOAD_STR                 'wait'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE   108  'to 108'

 L.  31        54  LOAD_FAST                'self'
               56  LOAD_ATTR                log
               58  LOAD_METHOD              warning

 L.  32        60  LOAD_STR                 'Redirect to \n%s\nVisit this URL in your browser, solve the CAPTCHA, and press ENTER to continue'

 L.  33        62  LOAD_FAST                'response'
               64  LOAD_ATTR                url
               66  CALL_METHOD_2         2  '2 positional arguments'
               68  POP_TOP          

 L.  34        70  SETUP_EXCEPT         82  'to 82'

 L.  35        72  LOAD_GLOBAL              input
               74  CALL_FUNCTION_0       0  '0 positional arguments'
               76  POP_TOP          
               78  POP_BLOCK        
               80  JUMP_FORWARD        122  'to 122'
             82_0  COME_FROM_EXCEPT     70  '70'

 L.  36        82  DUP_TOP          
               84  LOAD_GLOBAL              EOFError
               86  LOAD_GLOBAL              OSError
               88  BUILD_TUPLE_2         2 
               90  COMPARE_OP               exception-match
               92  POP_JUMP_IF_FALSE   104  'to 104'
               94  POP_TOP          
               96  POP_TOP          
               98  POP_TOP          

 L.  37       100  POP_EXCEPT       
              102  JUMP_FORWARD        122  'to 122'
            104_0  COME_FROM            92  '92'
              104  END_FINALLY      
              106  JUMP_BACK             2  'to 2'
            108_0  COME_FROM            52  '52'

 L.  39       108  LOAD_GLOBAL              exception
              110  LOAD_METHOD              StopExtraction

 L.  40       112  LOAD_STR                 'Redirect to \n%s\nVisit this URL in your browser and solve the CAPTCHA to continue'

 L.  41       114  LOAD_FAST                'response'
              116  LOAD_ATTR                url
              118  CALL_METHOD_2         2  '2 positional arguments'
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           102  '102'
            122_1  COME_FROM            80  '80'
              122  JUMP_BACK             2  'to 2'
              124  POP_BLOCK        
            126_0  COME_FROM_LOOP        0  '0'

Parse error at or near `COME_FROM' instruction at offset 122_1


class ReadcomiconlineIssueExtractor(ReadcomiconlineBase, ChapterExtractor):
    __doc__ = 'Extractor for comic-issues from readcomiconline.to'
    subcategory = 'issue'
    pattern = '(?i)(?:https?://)?(?:www\\.)?readcomiconline\\.to(/Comic/[^/?#]+/[^/?#]+\\?id=(\\d+))'
    test = (
     'https://readcomiconline.to/Comic/W-i-t-c-h/Issue-130?id=22289',
     {'url':'2bbab6ec4fbc05d269cca420a82a9b5acda28682', 
      'keyword':'30fe110273e871305001f33c18634516a0a51421'})

    def __init__(self, match):
        ChapterExtractor.__init__selfmatch
        self.issue_id = match.group(2)

    def metadata(self, page):
        comic, pos = text.extract(page, '   - Read\r\n    ', '\r\n')
        iinfo, pos = text.extract(page, '    ', '\r\n', pos)
        match = re.match'(?:Issue )?#(\\d+)|(.+)'iinfo
        return {'comic':comic, 
         'issue':match.group(1) or match.group(2), 
         'issue_id':text.parse_int(self.issue_id), 
         'lang':'en', 
         'language':'English'}

    def images(self, page):
        return [(url, None) for url in text.extract_iter(page, 'lstImages.push("', '"')]


class ReadcomiconlineComicExtractor(ReadcomiconlineBase, MangaExtractor):
    __doc__ = 'Extractor for comics from readcomiconline.to'
    chapterclass = ReadcomiconlineIssueExtractor
    subcategory = 'comic'
    pattern = '(?i)(?:https?://)?(?:www\\.)?readcomiconline\\.to(/Comic/[^/?#]+/?)$'
    test = (
     (
      'https://readcomiconline.to/Comic/W-i-t-c-h',
      {'url':'e231bc2a293edb465133c37a8e36a7e7d94cab14', 
       'keyword':'3986248e4458fa44a201ec073c3684917f48ee0c'}),
     (
      'https://readcomiconline.to/Comic/Bazooka-Jules',
      {'url':'711674cb78ed10bd2557315f7a67552d01b33985', 
       'keyword':'f5ba5246cd787bb750924d9690cb1549199bd516'}))

    def chapters(self, page):
        results = []
        comic, pos = text.extract(page, ' class="barTitle">', '<')
        page, pos = text.extract(page, ' class="listing">', '</table>', pos)
        comic = comic.rpartition('information')[0].strip()
        needle = ' title="Read {} '.format(comic)
        comic = text.unescape(comic)
        for item in text.extract_iter(page, ' href="', ' comic online '):
            url, _, issue = item.partition(needle)
            url = url.rpartition('"')[0]
            if issue.startswith('Issue #'):
                issue = issue[7:]
            else:
                results.append((self.root + url,
                 {'comic':comic, 
                  'issue':issue,  'issue_id':text.parse_int(url.rpartition('=')[2]), 
                  'lang':'en', 
                  'language':'English'}))

        return results