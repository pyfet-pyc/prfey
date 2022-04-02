# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: requests\status_codes.py
__doc__ = "\nThe ``codes`` object defines a mapping from common names for HTTP statuses\nto their numerical codes, accessible either as attributes or as dictionary\nitems.\n\nExample::\n\n    >>> import requests\n    >>> requests.codes['temporary_redirect']\n    307\n    >>> requests.codes.teapot\n    418\n    >>> requests.codes['\\o/']\n    200\n\nSome codes have multiple names, and both upper- and lower-case versions of\nthe names are allowed. For example, ``codes.ok``, ``codes.OK``, and\n``codes.okay`` all correspond to the HTTP status code 200.\n"
from .structures import LookupDict
_codes = {100:('continue', ), 
 101:('switching_protocols', ), 
 102:('processing', ), 
 103:('checkpoint', ), 
 122:('uri_too_long', 'request_uri_too_long'), 
 200:('ok', 'okay', 'all_ok', 'all_okay', 'all_good', '\\o/', '✓'), 
 201:('created', ), 
 202:('accepted', ), 
 203:('non_authoritative_info', 'non_authoritative_information'), 
 204:('no_content', ), 
 205:('reset_content', 'reset'), 
 206:('partial_content', 'partial'), 
 207:('multi_status', 'multiple_status', 'multi_stati', 'multiple_stati'), 
 208:('already_reported', ), 
 226:('im_used', ), 
 300:('multiple_choices', ), 
 301:('moved_permanently', 'moved', '\\o-'), 
 302:('found', ), 
 303:('see_other', 'other'), 
 304:('not_modified', ), 
 305:('use_proxy', ), 
 306:('switch_proxy', ), 
 307:('temporary_redirect', 'temporary_moved', 'temporary'), 
 308:('permanent_redirect', 'resume_incomplete', 'resume'), 
 400:('bad_request', 'bad'), 
 401:('unauthorized', ), 
 402:('payment_required', 'payment'), 
 403:('forbidden', ), 
 404:('not_found', '-o-'), 
 405:('method_not_allowed', 'not_allowed'), 
 406:('not_acceptable', ), 
 407:('proxy_authentication_required', 'proxy_auth', 'proxy_authentication'), 
 408:('request_timeout', 'timeout'), 
 409:('conflict', ), 
 410:('gone', ), 
 411:('length_required', ), 
 412:('precondition_failed', 'precondition'), 
 413:('request_entity_too_large', ), 
 414:('request_uri_too_large', ), 
 415:('unsupported_media_type', 'unsupported_media', 'media_type'), 
 416:('requested_range_not_satisfiable', 'requested_range', 'range_not_satisfiable'), 
 417:('expectation_failed', ), 
 418:('im_a_teapot', 'teapot', 'i_am_a_teapot'), 
 421:('misdirected_request', ), 
 422:('unprocessable_entity', 'unprocessable'), 
 423:('locked', ), 
 424:('failed_dependency', 'dependency'), 
 425:('unordered_collection', 'unordered'), 
 426:('upgrade_required', 'upgrade'), 
 428:('precondition_required', 'precondition'), 
 429:('too_many_requests', 'too_many'), 
 431:('header_fields_too_large', 'fields_too_large'), 
 444:('no_response', 'none'), 
 449:('retry_with', 'retry'), 
 450:('blocked_by_windows_parental_controls', 'parental_controls'), 
 451:('unavailable_for_legal_reasons', 'legal_reasons'), 
 499:('client_closed_request', ), 
 500:('internal_server_error', 'server_error', '/o\\', '✗'), 
 501:('not_implemented', ), 
 502:('bad_gateway', ), 
 503:('service_unavailable', 'unavailable'), 
 504:('gateway_timeout', ), 
 505:('http_version_not_supported', 'http_version'), 
 506:('variant_also_negotiates', ), 
 507:('insufficient_storage', ), 
 509:('bandwidth_limit_exceeded', 'bandwidth'), 
 510:('not_extended', ), 
 511:('network_authentication_required', 'network_auth', 'network_authentication')}
codes = LookupDict(name='status_codes')

def _init--- This code section failed: ---

 L. 108         0  LOAD_GLOBAL              _codes
                2  LOAD_METHOD              items
                4  CALL_METHOD_0         0  ''
                6  GET_ITER         
              8_0  COME_FROM            64  '64'
                8  FOR_ITER             66  'to 66'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'code'
               14  STORE_FAST               'titles'

 L. 109        16  LOAD_FAST                'titles'
               18  GET_ITER         
             20_0  COME_FROM            62  '62'
             20_1  COME_FROM            44  '44'
               20  FOR_ITER             64  'to 64'
               22  STORE_FAST               'title'

 L. 110        24  LOAD_GLOBAL              setattr
               26  LOAD_GLOBAL              codes
               28  LOAD_FAST                'title'
               30  LOAD_FAST                'code'
               32  CALL_FUNCTION_3       3  ''
               34  POP_TOP          

 L. 111        36  LOAD_FAST                'title'
               38  LOAD_METHOD              startswith
               40  LOAD_CONST               ('\\', '/')
               42  CALL_METHOD_1         1  ''
               44  POP_JUMP_IF_TRUE_BACK    20  'to 20'

 L. 112        46  LOAD_GLOBAL              setattr
               48  LOAD_GLOBAL              codes
               50  LOAD_FAST                'title'
               52  LOAD_METHOD              upper
               54  CALL_METHOD_0         0  ''
               56  LOAD_FAST                'code'
               58  CALL_FUNCTION_3       3  ''
               60  POP_TOP          
               62  JUMP_BACK            20  'to 20'
             64_0  COME_FROM            20  '20'
               64  JUMP_BACK             8  'to 8'
             66_0  COME_FROM             8  '8'

 L. 114        66  LOAD_CODE                <code_object doc>
               68  LOAD_STR                 '_init.<locals>.doc'
               70  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               72  STORE_DEREF              'doc'

 L. 121        74  LOAD_GLOBAL              __doc__
               76  LOAD_CONST               None
               78  <117>                 1  ''

 L. 119        80  POP_JUMP_IF_FALSE   118  'to 118'
               82  LOAD_GLOBAL              __doc__
               84  LOAD_STR                 '\n'
               86  BINARY_ADD       

 L. 120        88  LOAD_STR                 '\n'
               90  LOAD_METHOD              join
               92  LOAD_CLOSURE             'doc'
               94  BUILD_TUPLE_1         1 
               96  LOAD_GENEXPR             '<code_object <genexpr>>'
               98  LOAD_STR                 '_init.<locals>.<genexpr>'
              100  MAKE_FUNCTION_8          'closure'
              102  LOAD_GLOBAL              sorted
              104  LOAD_GLOBAL              _codes
              106  CALL_FUNCTION_1       1  ''
              108  GET_ITER         
              110  CALL_FUNCTION_1       1  ''
              112  CALL_METHOD_1         1  ''

 L. 119       114  BINARY_ADD       
              116  JUMP_FORWARD        120  'to 120'
            118_0  COME_FROM            80  '80'

 L. 121       118  LOAD_CONST               None
            120_0  COME_FROM           116  '116'

 L. 119       120  STORE_GLOBAL             __doc__

Parse error at or near `<117>' instruction at offset 78


_init()
# global __doc__ ## Warning: Unused global