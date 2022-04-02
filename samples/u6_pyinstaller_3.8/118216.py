# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\mechanize\_opener.py
"""URL opener.

Copyright 2004-2006 John J Lee <jjl@pobox.com>

This code is free software; you can redistribute it and/or modify it
under the terms of the BSD or ZPL 2.1 licenses (see the file
LICENSE included with the distribution).

"""
from __future__ import absolute_import
import bisect, os, tempfile, threading
from . import _response
from . import _rfc3986
from . import _sockettimeout
from . import _urllib2_fork
from ._request import Request
from ._util import isstringlike
from .polyglot import HTTPError, URLError, iteritems, is_class
open_file = open

class ContentTooShortError(URLError):

    def __init__(self, reason, result):
        URLError.__init__(self, reason)
        self.result = result


def set_request_attr(req, name, value, default):
    try:
        getattr(req, name)
    except AttributeError:
        setattr(req, name, default)
    else:
        if value is not default:
            setattr(req, name, value)


class OpenerDirector(_urllib2_fork.OpenerDirector):

    def __init__(self):
        _urllib2_fork.OpenerDirector.__init__(self)
        self.process_response = {}
        self.process_request = {}
        self._any_request = {}
        self._any_response = {}
        self._handler_index_valid = True
        self._tempfiles = []

    def add_handler(self, handler):
        if not hasattr(handler, 'add_parent'):
            raise TypeError('expected BaseHandler instance, got %r' % type(handler))
        if handler in self.handlers:
            return
        bisect.insort(self.handlers, handler)
        handler.add_parent(self)
        self._handler_index_valid = False

    def _maybe_reindex_handlers--- This code section failed: ---

 L.  72         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _handler_index_valid
                4  POP_JUMP_IF_FALSE    10  'to 10'

 L.  73         6  LOAD_CONST               None
                8  RETURN_VALUE     
             10_0  COME_FROM             4  '4'

 L.  75        10  BUILD_MAP_0           0 
               12  STORE_FAST               'handle_error'

 L.  76        14  BUILD_MAP_0           0 
               16  STORE_FAST               'handle_open'

 L.  77        18  BUILD_MAP_0           0 
               20  STORE_FAST               'process_request'

 L.  78        22  BUILD_MAP_0           0 
               24  STORE_FAST               'process_response'

 L.  79        26  LOAD_GLOBAL              set
               28  CALL_FUNCTION_0       0  ''
               30  STORE_FAST               'any_request'

 L.  80        32  LOAD_GLOBAL              set
               34  CALL_FUNCTION_0       0  ''
               36  STORE_FAST               'any_response'

 L.  81        38  BUILD_LIST_0          0 
               40  STORE_FAST               'unwanted'

 L.  83        42  LOAD_FAST                'self'
               44  LOAD_ATTR                handlers
               46  GET_ITER         
             48_0  COME_FROM           366  '366'
            48_50  FOR_ITER            380  'to 380'
               52  STORE_FAST               'handler'

 L.  84        54  LOAD_CONST               False
               56  STORE_FAST               'added'

 L.  85        58  LOAD_GLOBAL              dir
               60  LOAD_FAST                'handler'
               62  CALL_FUNCTION_1       1  ''
               64  GET_ITER         
             66_0  COME_FROM           324  '324'
            66_68  FOR_ITER            364  'to 364'
               70  STORE_FAST               'meth'

 L.  86        72  LOAD_FAST                'meth'
               74  LOAD_CONST               ('redirect_request', 'do_open', 'proxy_open')
               76  COMPARE_OP               in
               78  POP_JUMP_IF_FALSE    82  'to 82'

 L.  88        80  JUMP_BACK            66  'to 66'
             82_0  COME_FROM            78  '78'

 L.  90        82  LOAD_FAST                'meth'
               84  LOAD_STR                 'any_request'
               86  COMPARE_OP               ==
               88  POP_JUMP_IF_FALSE   108  'to 108'

 L.  91        90  LOAD_FAST                'any_request'
               92  LOAD_METHOD              add
               94  LOAD_FAST                'handler'
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          

 L.  92       100  LOAD_CONST               True
              102  STORE_FAST               'added'

 L.  93       104  JUMP_BACK            66  'to 66'
              106  JUMP_FORWARD        132  'to 132'
            108_0  COME_FROM            88  '88'

 L.  94       108  LOAD_FAST                'meth'
              110  LOAD_STR                 'any_response'
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   132  'to 132'

 L.  95       116  LOAD_FAST                'any_response'
              118  LOAD_METHOD              add
              120  LOAD_FAST                'handler'
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L.  96       126  LOAD_CONST               True
              128  STORE_FAST               'added'

 L.  97       130  JUMP_BACK            66  'to 66'
            132_0  COME_FROM           114  '114'
            132_1  COME_FROM           106  '106'

 L.  99       132  LOAD_FAST                'meth'
              134  LOAD_METHOD              find
              136  LOAD_STR                 '_'
              138  CALL_METHOD_1         1  ''
              140  STORE_FAST               'ii'

 L. 100       142  LOAD_FAST                'meth'
              144  LOAD_CONST               None
              146  LOAD_FAST                'ii'
              148  BUILD_SLICE_2         2 
              150  BINARY_SUBSCR    
              152  STORE_FAST               'scheme'

 L. 101       154  LOAD_FAST                'meth'
              156  LOAD_FAST                'ii'
              158  LOAD_CONST               1
              160  BINARY_ADD       
              162  LOAD_CONST               None
              164  BUILD_SLICE_2         2 
              166  BINARY_SUBSCR    
              168  STORE_FAST               'condition'

 L. 103       170  LOAD_FAST                'condition'
              172  LOAD_METHOD              startswith
              174  LOAD_STR                 'error'
              176  CALL_METHOD_1         1  ''
          178_180  POP_JUMP_IF_FALSE   278  'to 278'

 L. 104       182  LOAD_FAST                'meth'
              184  LOAD_FAST                'ii'
              186  LOAD_CONST               1
              188  BINARY_ADD       
              190  LOAD_CONST               None
              192  BUILD_SLICE_2         2 
              194  BINARY_SUBSCR    
              196  LOAD_METHOD              find
              198  LOAD_STR                 '_'
              200  CALL_METHOD_1         1  ''
              202  LOAD_FAST                'ii'
              204  BINARY_ADD       
              206  LOAD_CONST               1
              208  BINARY_ADD       
              210  STORE_FAST               'jj'

 L. 105       212  LOAD_FAST                'meth'
              214  LOAD_FAST                'jj'
              216  LOAD_CONST               1
              218  BINARY_ADD       
              220  LOAD_CONST               None
              222  BUILD_SLICE_2         2 
              224  BINARY_SUBSCR    
              226  STORE_FAST               'kind'

 L. 106       228  SETUP_FINALLY       242  'to 242'

 L. 107       230  LOAD_GLOBAL              int
              232  LOAD_FAST                'kind'
              234  CALL_FUNCTION_1       1  ''
              236  STORE_FAST               'kind'
              238  POP_BLOCK        
              240  JUMP_FORWARD        264  'to 264'
            242_0  COME_FROM_FINALLY   228  '228'

 L. 108       242  DUP_TOP          
              244  LOAD_GLOBAL              ValueError
              246  COMPARE_OP               exception-match
          248_250  POP_JUMP_IF_FALSE   262  'to 262'
              252  POP_TOP          
              254  POP_TOP          
              256  POP_TOP          

 L. 109       258  POP_EXCEPT       
              260  JUMP_FORWARD        264  'to 264'
            262_0  COME_FROM           248  '248'
              262  END_FINALLY      
            264_0  COME_FROM           260  '260'
            264_1  COME_FROM           240  '240'

 L. 110       264  LOAD_FAST                'handle_error'
              266  LOAD_METHOD              setdefault
              268  LOAD_FAST                'scheme'
              270  BUILD_MAP_0           0 
              272  CALL_METHOD_2         2  ''
              274  STORE_FAST               'lookup'
              276  JUMP_FORWARD        338  'to 338'
            278_0  COME_FROM           178  '178'

 L. 111       278  LOAD_FAST                'condition'
              280  LOAD_STR                 'open'
              282  COMPARE_OP               ==
          284_286  POP_JUMP_IF_FALSE   298  'to 298'

 L. 112       288  LOAD_FAST                'scheme'
              290  STORE_FAST               'kind'

 L. 113       292  LOAD_FAST                'handle_open'
              294  STORE_FAST               'lookup'
              296  JUMP_FORWARD        338  'to 338'
            298_0  COME_FROM           284  '284'

 L. 114       298  LOAD_FAST                'condition'
              300  LOAD_STR                 'request'
              302  COMPARE_OP               ==
          304_306  POP_JUMP_IF_FALSE   318  'to 318'

 L. 115       308  LOAD_FAST                'scheme'
              310  STORE_FAST               'kind'

 L. 116       312  LOAD_FAST                'process_request'
              314  STORE_FAST               'lookup'
              316  JUMP_FORWARD        338  'to 338'
            318_0  COME_FROM           304  '304'

 L. 117       318  LOAD_FAST                'condition'
              320  LOAD_STR                 'response'
              322  COMPARE_OP               ==
              324  POP_JUMP_IF_FALSE    66  'to 66'

 L. 118       326  LOAD_FAST                'scheme'
              328  STORE_FAST               'kind'

 L. 119       330  LOAD_FAST                'process_response'
              332  STORE_FAST               'lookup'
              334  JUMP_FORWARD        338  'to 338'

 L. 121       336  JUMP_BACK            66  'to 66'
            338_0  COME_FROM           334  '334'
            338_1  COME_FROM           316  '316'
            338_2  COME_FROM           296  '296'
            338_3  COME_FROM           276  '276'

 L. 123       338  LOAD_FAST                'lookup'
              340  LOAD_METHOD              setdefault
              342  LOAD_FAST                'kind'
              344  LOAD_GLOBAL              set
              346  CALL_FUNCTION_0       0  ''
              348  CALL_METHOD_2         2  ''
              350  LOAD_METHOD              add
              352  LOAD_FAST                'handler'
              354  CALL_METHOD_1         1  ''
              356  POP_TOP          

 L. 124       358  LOAD_CONST               True
              360  STORE_FAST               'added'
              362  JUMP_BACK            66  'to 66'

 L. 126       364  LOAD_FAST                'added'
              366  POP_JUMP_IF_TRUE     48  'to 48'

 L. 127       368  LOAD_FAST                'unwanted'
              370  LOAD_METHOD              append
              372  LOAD_FAST                'handler'
              374  CALL_METHOD_1         1  ''
              376  POP_TOP          
              378  JUMP_BACK            48  'to 48'

 L. 129       380  LOAD_FAST                'unwanted'
              382  GET_ITER         
              384  FOR_ITER            404  'to 404'
              386  STORE_FAST               'handler'

 L. 130       388  LOAD_FAST                'self'
              390  LOAD_ATTR                handlers
              392  LOAD_METHOD              remove
              394  LOAD_FAST                'handler'
              396  CALL_METHOD_1         1  ''
              398  POP_TOP          
          400_402  JUMP_BACK           384  'to 384'

 L. 134       404  LOAD_FAST                'process_request'
              406  LOAD_FAST                'process_response'
              408  BUILD_TUPLE_2         2 
              410  GET_ITER         
              412  FOR_ITER            448  'to 448'
              414  STORE_FAST               'lookup'

 L. 135       416  LOAD_GLOBAL              iteritems
              418  LOAD_FAST                'lookup'
              420  CALL_FUNCTION_1       1  ''
              422  GET_ITER         
              424  FOR_ITER            444  'to 444'
              426  UNPACK_SEQUENCE_2     2 
              428  STORE_FAST               'scheme'
              430  STORE_FAST               'handlers'

 L. 136       432  LOAD_FAST                'handlers'
              434  LOAD_FAST                'lookup'
              436  LOAD_FAST                'scheme'
              438  STORE_SUBSCR     
          440_442  JUMP_BACK           424  'to 424'
          444_446  JUMP_BACK           412  'to 412'

 L. 137       448  LOAD_GLOBAL              iteritems
              450  LOAD_FAST                'handle_error'
              452  CALL_FUNCTION_1       1  ''
              454  GET_ITER         
              456  FOR_ITER            512  'to 512'
              458  UNPACK_SEQUENCE_2     2 
              460  STORE_FAST               'scheme'
              462  STORE_FAST               'lookup'

 L. 138       464  LOAD_GLOBAL              iteritems
              466  LOAD_FAST                'lookup'
              468  CALL_FUNCTION_1       1  ''
              470  GET_ITER         
              472  FOR_ITER            508  'to 508'
              474  UNPACK_SEQUENCE_2     2 
              476  STORE_FAST               'code'
              478  STORE_FAST               'handlers'

 L. 139       480  LOAD_GLOBAL              list
              482  LOAD_FAST                'handlers'
              484  CALL_FUNCTION_1       1  ''
              486  STORE_FAST               'handlers'

 L. 140       488  LOAD_FAST                'handlers'
              490  LOAD_METHOD              sort
              492  CALL_METHOD_0         0  ''
              494  POP_TOP          

 L. 141       496  LOAD_FAST                'handlers'
              498  LOAD_FAST                'lookup'
              500  LOAD_FAST                'code'
              502  STORE_SUBSCR     
          504_506  JUMP_BACK           472  'to 472'
          508_510  JUMP_BACK           456  'to 456'

 L. 142       512  LOAD_GLOBAL              iteritems
              514  LOAD_FAST                'handle_open'
              516  CALL_FUNCTION_1       1  ''
              518  GET_ITER         
              520  FOR_ITER            556  'to 556'
              522  UNPACK_SEQUENCE_2     2 
              524  STORE_FAST               'scheme'
              526  STORE_FAST               'handlers'

 L. 143       528  LOAD_GLOBAL              list
              530  LOAD_FAST                'handlers'
              532  CALL_FUNCTION_1       1  ''
              534  STORE_FAST               'handlers'

 L. 144       536  LOAD_FAST                'handlers'
              538  LOAD_METHOD              sort
              540  CALL_METHOD_0         0  ''
              542  POP_TOP          

 L. 145       544  LOAD_FAST                'handlers'
              546  LOAD_FAST                'handle_open'
              548  LOAD_FAST                'scheme'
              550  STORE_SUBSCR     
          552_554  JUMP_BACK           520  'to 520'

 L. 148       556  LOAD_FAST                'handle_error'
              558  LOAD_FAST                'self'
              560  STORE_ATTR               handle_error

 L. 149       562  LOAD_FAST                'handle_open'
              564  LOAD_FAST                'self'
              566  STORE_ATTR               handle_open

 L. 150       568  LOAD_FAST                'process_request'
              570  LOAD_FAST                'self'
              572  STORE_ATTR               process_request

 L. 151       574  LOAD_FAST                'process_response'
              576  LOAD_FAST                'self'
              578  STORE_ATTR               process_response

 L. 152       580  LOAD_FAST                'any_request'
              582  LOAD_FAST                'self'
              584  STORE_ATTR               _any_request

 L. 153       586  LOAD_FAST                'any_response'
              588  LOAD_FAST                'self'
              590  STORE_ATTR               _any_response

Parse error at or near `COME_FROM' instruction at offset 338_0

    def _request(self, url_or_req, data, visit, timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        if isstringlike(url_or_req):
            req = Request(url_or_req, data, visit=visit, timeout=timeout)
        else:
            req = url_or_req
            if data is not None:
                req.add_data(data)
            set_request_attr(req, 'visit', visit, None)
            set_request_attr(req, 'timeout', timeout, _sockettimeout._GLOBAL_DEFAULT_TIMEOUT)
        return req

    def open(self, fullurl, data=None, timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
        req = self._request(fullurl, data, None, timeout)
        req_scheme = req.get_type()
        self._maybe_reindex_handlers()
        request_processors = set(self.process_request.get(req_scheme, []))
        request_processors.update(self._any_request)
        request_processors = list(request_processors)
        request_processors.sort()
        for processor in request_processors:
            for meth_name in (
             'any_request', req_scheme + '_request'):
                meth = getattr(processor, meth_name, None)
                if meth:
                    req = meth(req)
            else:
                urlopen = _urllib2_fork.OpenerDirector._open
                response = urlopen(self, req, data)
                response_processors = set(self.process_response.get(req_scheme, []))
                response_processors.update(self._any_response)
                response_processors = list(response_processors)
                response_processors.sort()
                for processor in response_processors:
                    for meth_name in (
                     'any_response', req_scheme + '_response'):
                        meth = getattr(processor, meth_name, None)
                        if meth:
                            response = meth(req, response)
                    else:
                        return response

    def error(self, proto, *args):
        if proto in ('http', 'https'):
            dict = self.handle_error['http']
            proto = args[2]
            meth_name = 'http_error_%s' % proto
            http_err = 1
            orig_args = args
        else:
            dict = self.handle_error
            meth_name = proto + '_error'
            http_err = 0
        args = (
         dict, proto, meth_name) + args
        result = (self._call_chain)(*args)
        if result:
            return result
        if http_err:
            args = (
             dict, 'default', 'http_error_default') + orig_args
            return (self._call_chain)(*args)

    BLOCK_SIZE = 8192

    def retrieve--- This code section failed: ---

 L. 250         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _request
                4  LOAD_FAST                'fullurl'
                6  LOAD_FAST                'data'
                8  LOAD_CONST               False
               10  LOAD_FAST                'timeout'
               12  CALL_METHOD_4         4  ''
               14  STORE_FAST               'req'

 L. 251        16  LOAD_FAST                'req'
               18  LOAD_METHOD              get_type
               20  CALL_METHOD_0         0  ''
               22  STORE_FAST               'scheme'

 L. 252        24  LOAD_FAST                'self'
               26  LOAD_METHOD              open
               28  LOAD_FAST                'req'
               30  CALL_METHOD_1         1  ''
               32  STORE_FAST               'fp'

 L. 253     34_36  SETUP_FINALLY       310  'to 310'

 L. 254        38  LOAD_FAST                'fp'
               40  LOAD_METHOD              info
               42  CALL_METHOD_0         0  ''
               44  STORE_FAST               'headers'

 L. 255        46  LOAD_FAST                'filename'
               48  LOAD_CONST               None
               50  COMPARE_OP               is
               52  POP_JUMP_IF_FALSE    74  'to 74'
               54  LOAD_FAST                'scheme'
               56  LOAD_STR                 'file'
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE    74  'to 74'

 L. 258        62  LOAD_CONST               None
               64  LOAD_FAST                'headers'
               66  BUILD_TUPLE_2         2 
               68  POP_BLOCK        
               70  CALL_FINALLY        310  'to 310'
               72  RETURN_VALUE     
             74_0  COME_FROM            60  '60'
             74_1  COME_FROM            52  '52'

 L. 260        74  LOAD_FAST                'filename'
               76  POP_JUMP_IF_FALSE    90  'to 90'

 L. 261        78  LOAD_FAST                'open'
               80  LOAD_FAST                'filename'
               82  LOAD_STR                 'wb'
               84  CALL_FUNCTION_2       2  ''
               86  STORE_FAST               'tfp'
               88  JUMP_FORWARD        162  'to 162'
             90_0  COME_FROM            76  '76'

 L. 263        90  LOAD_GLOBAL              _rfc3986
               92  LOAD_METHOD              urlsplit
               94  LOAD_FAST                'req'
               96  LOAD_METHOD              get_full_url
               98  CALL_METHOD_0         0  ''
              100  CALL_METHOD_1         1  ''
              102  LOAD_CONST               2
              104  BINARY_SUBSCR    
              106  STORE_FAST               'path'

 L. 264       108  LOAD_GLOBAL              os
              110  LOAD_ATTR                path
              112  LOAD_METHOD              splitext
              114  LOAD_FAST                'path'
              116  CALL_METHOD_1         1  ''
              118  LOAD_CONST               1
              120  BINARY_SUBSCR    
              122  STORE_FAST               'suffix'

 L. 265       124  LOAD_GLOBAL              tempfile
              126  LOAD_METHOD              mkstemp
              128  LOAD_FAST                'suffix'
              130  CALL_METHOD_1         1  ''
              132  UNPACK_SEQUENCE_2     2 
              134  STORE_FAST               'fd'
              136  STORE_FAST               'filename'

 L. 266       138  LOAD_FAST                'self'
              140  LOAD_ATTR                _tempfiles
              142  LOAD_METHOD              append
              144  LOAD_FAST                'filename'
              146  CALL_METHOD_1         1  ''
              148  POP_TOP          

 L. 267       150  LOAD_GLOBAL              os
              152  LOAD_METHOD              fdopen
              154  LOAD_FAST                'fd'
              156  LOAD_STR                 'wb'
              158  CALL_METHOD_2         2  ''
              160  STORE_FAST               'tfp'
            162_0  COME_FROM            88  '88'

 L. 268       162  SETUP_FINALLY       296  'to 296'

 L. 269       164  LOAD_FAST                'filename'
              166  LOAD_FAST                'headers'
              168  BUILD_TUPLE_2         2 
              170  STORE_FAST               'result'

 L. 270       172  LOAD_FAST                'self'
              174  LOAD_ATTR                BLOCK_SIZE
              176  STORE_FAST               'bs'

 L. 271       178  LOAD_CONST               -1
              180  STORE_FAST               'size'

 L. 272       182  LOAD_CONST               0
              184  STORE_FAST               'read'

 L. 273       186  LOAD_CONST               0
              188  STORE_FAST               'blocknum'

 L. 274       190  LOAD_FAST                'reporthook'
              192  POP_JUMP_IF_FALSE   226  'to 226'

 L. 275       194  LOAD_STR                 'content-length'
              196  LOAD_FAST                'headers'
              198  COMPARE_OP               in
              200  POP_JUMP_IF_FALSE   214  'to 214'

 L. 276       202  LOAD_GLOBAL              int
              204  LOAD_FAST                'headers'
              206  LOAD_STR                 'content-length'
              208  BINARY_SUBSCR    
              210  CALL_FUNCTION_1       1  ''
              212  STORE_FAST               'size'
            214_0  COME_FROM           200  '200'

 L. 277       214  LOAD_FAST                'reporthook'
              216  LOAD_FAST                'blocknum'
              218  LOAD_FAST                'bs'
              220  LOAD_FAST                'size'
              222  CALL_FUNCTION_3       3  ''
              224  POP_TOP          
            226_0  COME_FROM           276  '276'
            226_1  COME_FROM           192  '192'

 L. 279       226  LOAD_FAST                'fp'
              228  LOAD_METHOD              read
              230  LOAD_FAST                'bs'
              232  CALL_METHOD_1         1  ''
              234  STORE_FAST               'block'

 L. 280       236  LOAD_FAST                'block'
              238  POP_JUMP_IF_TRUE    244  'to 244'

 L. 281   240_242  BREAK_LOOP          292  'to 292'
            244_0  COME_FROM           238  '238'

 L. 282       244  LOAD_FAST                'read'
              246  LOAD_GLOBAL              len
              248  LOAD_FAST                'block'
              250  CALL_FUNCTION_1       1  ''
              252  INPLACE_ADD      
              254  STORE_FAST               'read'

 L. 283       256  LOAD_FAST                'tfp'
              258  LOAD_METHOD              write
              260  LOAD_FAST                'block'
              262  CALL_METHOD_1         1  ''
              264  POP_TOP          

 L. 284       266  LOAD_FAST                'blocknum'
              268  LOAD_CONST               1
              270  INPLACE_ADD      
              272  STORE_FAST               'blocknum'

 L. 285       274  LOAD_FAST                'reporthook'
              276  POP_JUMP_IF_FALSE   226  'to 226'

 L. 286       278  LOAD_FAST                'reporthook'
              280  LOAD_FAST                'blocknum'
              282  LOAD_FAST                'bs'
              284  LOAD_FAST                'size'
              286  CALL_FUNCTION_3       3  ''
              288  POP_TOP          
              290  JUMP_BACK           226  'to 226'
              292  POP_BLOCK        
              294  BEGIN_FINALLY    
            296_0  COME_FROM_FINALLY   162  '162'

 L. 288       296  LOAD_FAST                'tfp'
              298  LOAD_METHOD              close
              300  CALL_METHOD_0         0  ''
              302  POP_TOP          
              304  END_FINALLY      
              306  POP_BLOCK        
              308  BEGIN_FINALLY    
            310_0  COME_FROM            70  '70'
            310_1  COME_FROM_FINALLY    34  '34'

 L. 290       310  LOAD_FAST                'fp'
              312  LOAD_METHOD              close
              314  CALL_METHOD_0         0  ''
              316  POP_TOP          
              318  END_FINALLY      

 L. 293       320  LOAD_FAST                'size'
              322  LOAD_CONST               0
              324  COMPARE_OP               >=
          326_328  POP_JUMP_IF_FALSE   358  'to 358'
              330  LOAD_FAST                'read'
              332  LOAD_FAST                'size'
              334  COMPARE_OP               <
          336_338  POP_JUMP_IF_FALSE   358  'to 358'

 L. 294       340  LOAD_GLOBAL              ContentTooShortError

 L. 295       342  LOAD_STR                 'retrieval incomplete: got only %i out of %i bytes'

 L. 296       344  LOAD_FAST                'read'
              346  LOAD_FAST                'size'
              348  BUILD_TUPLE_2         2 

 L. 295       350  BINARY_MODULO    

 L. 297       352  LOAD_FAST                'result'

 L. 294       354  CALL_FUNCTION_2       2  ''
              356  RAISE_VARARGS_1       1  'exception instance'
            358_0  COME_FROM           336  '336'
            358_1  COME_FROM           326  '326'

 L. 300       358  LOAD_FAST                'result'
              360  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `CALL_FINALLY' instruction at offset 70

    def close(self):
        _urllib2_fork.OpenerDirector.close(self)
        self.open = self.error = self.retrieve = self.add_handler = None
        if self._tempfiles:
            for filename in self._tempfiles:
                try:
                    os.unlink(filename)
                except OSError:
                    pass

            else:
                del self._tempfiles[:]


def wrapped_open(urlopen, process_response_object, fullurl, data=None, timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
    success = True
    try:
        response = urlopen(fullurl, data, timeout)
    except HTTPError as error:
        try:
            success = False
            if error.fp is None:
                raise
            response = error
        finally:
            error = None
            del error

    else:
        if response is not None:
            response = process_response_object(response)
        if not success:
            raise response
        return response


class ResponseProcessingOpener(OpenerDirector):

    def open(self, fullurl, data=None, timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):

        def bound_open(fullurl, data=None, timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
            return OpenerDirector.open(self, fullurl, data, timeout)

        return wrapped_open(bound_open, self.process_response_object, fullurl, data, timeout)

    def process_response_object(self, response):
        return response


class SeekableResponseOpener(ResponseProcessingOpener):

    def process_response_object(self, response):
        return _response.seek_wrapped_response(response)


class OpenerFactory:
    __doc__ = "This class's interface is quite likely to change."
    default_classes = [
     _urllib2_fork.ProxyHandler,
     _urllib2_fork.UnknownHandler,
     _urllib2_fork.HTTPHandler,
     _urllib2_fork.HTTPDefaultErrorHandler,
     _urllib2_fork.HTTPRedirectHandler,
     _urllib2_fork.FTPHandler,
     _urllib2_fork.FileHandler,
     _urllib2_fork.HTTPCookieProcessor,
     _urllib2_fork.HTTPErrorProcessor]
    default_classes.append(_urllib2_fork.HTTPSHandler)
    handlers = []
    replacement_handlers = []

    def __init__(self, klass=OpenerDirector):
        self.klass = klass

    def build_opener(self, *handlers):
        """Create an opener object from a list of handlers and processors.

        The opener will use several default handlers and processors, including
        support for HTTP and FTP.

        If any of the handlers passed as arguments are subclasses of the
        default handlers, the default handlers will not be used.

        """
        opener = self.klass()
        default_classes = list(self.default_classes)
        skip = set()
        for klass in default_classes:
            for check in handlers:
                if is_class(check):
                    if issubclass(check, klass):
                        skip.add(klass)
                elif isinstance(check, klass):
                    skip.add(klass)

        for klass in skip:
            default_classes.remove(klass)
        else:
            for klass in default_classes:
                opener.add_handler(klass())
            else:
                for h in handlers:
                    if is_class(h):
                        h = h()
                    opener.add_handler(h)
                else:
                    return opener


build_opener = OpenerFactory().build_opener
thread_local = threading.local()
thread_local.opener = None

def get_thread_local_opener():
    try:
        ans = thread_local.opener
    except AttributeError:
        ans = getattr(get_thread_local_opener, 'ans', None)
        if ans is None:
            ans = get_thread_local_opener.ans = build_opener()
    else:
        if ans is None:
            ans = thread_local.opener = build_opener()
        return ans


def urlopen(url, data=None, timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
    return get_thread_local_opener().open(url, data, timeout)


def urlretrieve(url, filename=None, reporthook=None, data=None, timeout=_sockettimeout._GLOBAL_DEFAULT_TIMEOUT):
    return get_thread_local_opener().retrieve(url, filename, reporthook, data, timeout)


def install_opener(opener):
    get_thread_local_opener.ans = opener
    try:
        thread_local.opener = opener
    except AttributeError:
        pass