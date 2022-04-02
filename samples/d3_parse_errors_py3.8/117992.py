# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\discord\webhook.py
"""
The MIT License (MIT)

Copyright (c) 2015-2020 Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
import asyncio, json, time, re, aiohttp
from . import utils
from .errors import InvalidArgument, HTTPException, Forbidden, NotFound
from .enums import try_enum, WebhookType
from .user import BaseUser, User
from .asset import Asset
__all__ = ('WebhookAdapter', 'AsyncWebhookAdapter', 'RequestsWebhookAdapter', 'Webhook')

class WebhookAdapter:
    __doc__ = 'Base class for all webhook adapters.\n\n    Attributes\n    ------------\n    webhook: :class:`Webhook`\n        The webhook that owns this adapter.\n    '
    BASE = 'https://discordapp.com/api/v7'

    def _prepare(self, webhook):
        self._webhook_id = webhook.id
        self._webhook_token = webhook.token
        self._request_url = '{0.BASE}/webhooks/{1}/{2}'.format(self, webhook.id, webhook.token)
        self.webhook = webhook

    def request(self, verb, url, payload=None, multipart=None):
        """Actually does the request.

        Subclasses must implement this.

        Parameters
        -----------
        verb: :class:`str`
            The HTTP verb to use for the request.
        url: :class:`str`
            The URL to send the request to. This will have
            the query parameters already added to it, if any.
        multipart: Optional[:class:`dict`]
            A dict containing multipart form data to send with
            the request. If a filename is being uploaded, then it will
            be under a ``file`` key which will have a 3-element :class:`tuple`
            denoting ``(filename, file, content_type)``.
        payload: Optional[:class:`dict`]
            The JSON to send with the request, if any.
        """
        raise NotImplementedError()

    def delete_webhook(self):
        return self.request('DELETE', self._request_url)

    def edit_webhook(self, **payload):
        return self.request('PATCH', (self._request_url), payload=payload)

    def handle_execution_response(self, data, *, wait):
        """Transforms the webhook execution response into something
        more meaningful.

        This is mainly used to convert the data into a :class:`Message`
        if necessary.

        Subclasses must implement this.

        Parameters
        ------------
        data
            The data that was returned from the request.
        wait: :class:`bool`
            Whether the webhook execution was asked to wait or not.
        """
        raise NotImplementedError()

    async def _wrap_coroutine_and_cleanup(self, coro, cleanup):
        try:
            return await coro
        finally:
            cleanup()

    def execute_webhook(self, *, payload, wait=False, file=None, files=None):
        cleanup = None
        if file is not None:
            multipart = {'file':(file.filename, file.fp, 'application/octet-stream'),  'payload_json':utils.to_json(payload)}
            data = None
            cleanup = file.close
            files_to_pass = [file]
        elif files is not None:
            multipart = {'payload_json': utils.to_json(payload)}
            for i, file in enumerate(files):
                multipart['file%i' % i] = (
                 file.filename, file.fp, 'application/octet-stream')
            else:
                data = None

                def _anon():
                    for f in files:
                        f.close()

                cleanup = _anon
                files_to_pass = files

        else:
            data = payload
            multipart = None
            files_to_pass = None
        url = '%s?wait=%d' % (self._request_url, wait)
        maybe_coro = None
        try:
            maybe_coro = self.request('POST', url, multipart=multipart, payload=data, files=files_to_pass)
        finally:
            if maybe_coro is not None:
                if cleanup is not None:
                    if not asyncio.iscoroutine(maybe_coro):
                        cleanup()
                    else:
                        maybe_coro = self._wrap_coroutine_and_cleanup(maybe_coro, cleanup)

        return self.handle_execution_response(maybe_coro, wait=wait)


class AsyncWebhookAdapter(WebhookAdapter):
    __doc__ = 'A webhook adapter suited for use with aiohttp.\n\n    .. note::\n\n        You are responsible for cleaning up the client session.\n\n    Parameters\n    -----------\n    session: :class:`aiohttp.ClientSession`\n        The session to use to send requests.\n    '

    def __init__(self, session):
        self.session = session
        self.loop = asyncio.get_event_loop()

    async def request--- This code section failed: ---

 L. 177         0  BUILD_MAP_0           0 
                2  STORE_FAST               'headers'

 L. 178         4  LOAD_CONST               None
                6  STORE_FAST               'data'

 L. 179         8  LOAD_FAST                'files'
               10  JUMP_IF_TRUE_OR_POP    14  'to 14'
               12  BUILD_LIST_0          0 
             14_0  COME_FROM            10  '10'
               14  STORE_FAST               'files'

 L. 180        16  LOAD_FAST                'payload'
               18  POP_JUMP_IF_FALSE    38  'to 38'

 L. 181        20  LOAD_STR                 'application/json'
               22  LOAD_FAST                'headers'
               24  LOAD_STR                 'Content-Type'
               26  STORE_SUBSCR     

 L. 182        28  LOAD_GLOBAL              utils
               30  LOAD_METHOD              to_json
               32  LOAD_FAST                'payload'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'data'
             38_0  COME_FROM            18  '18'

 L. 184        38  LOAD_FAST                'multipart'
               40  POP_JUMP_IF_FALSE   122  'to 122'

 L. 185        42  LOAD_GLOBAL              aiohttp
               44  LOAD_METHOD              FormData
               46  CALL_METHOD_0         0  ''
               48  STORE_FAST               'data'

 L. 186        50  LOAD_FAST                'multipart'
               52  LOAD_METHOD              items
               54  CALL_METHOD_0         0  ''
               56  GET_ITER         
             58_0  COME_FROM           120  '120'
             58_1  COME_FROM           106  '106'
               58  FOR_ITER            122  'to 122'
               60  UNPACK_SEQUENCE_2     2 
               62  STORE_FAST               'key'
               64  STORE_FAST               'value'

 L. 187        66  LOAD_FAST                'key'
               68  LOAD_METHOD              startswith
               70  LOAD_STR                 'file'
               72  CALL_METHOD_1         1  ''
               74  POP_JUMP_IF_FALSE   108  'to 108'

 L. 188        76  LOAD_FAST                'data'
               78  LOAD_ATTR                add_field
               80  LOAD_FAST                'key'
               82  LOAD_FAST                'value'
               84  LOAD_CONST               1
               86  BINARY_SUBSCR    
               88  LOAD_FAST                'value'
               90  LOAD_CONST               0
               92  BINARY_SUBSCR    
               94  LOAD_FAST                'value'
               96  LOAD_CONST               2
               98  BINARY_SUBSCR    
              100  LOAD_CONST               ('filename', 'content_type')
              102  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              104  POP_TOP          
              106  JUMP_BACK            58  'to 58'
            108_0  COME_FROM            74  '74'

 L. 190       108  LOAD_FAST                'data'
              110  LOAD_METHOD              add_field
              112  LOAD_FAST                'key'
              114  LOAD_FAST                'value'
              116  CALL_METHOD_2         2  ''
              118  POP_TOP          
              120  JUMP_BACK            58  'to 58'
            122_0  COME_FROM            58  '58'
            122_1  COME_FROM            40  '40'

 L. 192       122  LOAD_GLOBAL              range
              124  LOAD_CONST               5
              126  CALL_FUNCTION_1       1  ''
              128  GET_ITER         
            130_0  COME_FROM           538  '538'
            130_1  COME_FROM           462  '462'
            130_2  COME_FROM           408  '408'
          130_132  FOR_ITER            540  'to 540'
              134  STORE_FAST               'tries'

 L. 193       136  LOAD_FAST                'files'
              138  GET_ITER         
            140_0  COME_FROM           156  '156'
              140  FOR_ITER            158  'to 158'
              142  STORE_FAST               'file'

 L. 194       144  LOAD_FAST                'file'
              146  LOAD_ATTR                reset
              148  LOAD_FAST                'tries'
              150  LOAD_CONST               ('seek',)
              152  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              154  POP_TOP          
              156  JUMP_BACK           140  'to 140'
            158_0  COME_FROM           140  '140'

 L. 196       158  LOAD_FAST                'self'
              160  LOAD_ATTR                session
              162  LOAD_ATTR                request
              164  LOAD_FAST                'verb'
              166  LOAD_FAST                'url'
              168  LOAD_FAST                'headers'
              170  LOAD_FAST                'data'
              172  LOAD_CONST               ('headers', 'data')
              174  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              176  BEFORE_ASYNC_WITH
              178  GET_AWAITABLE    
              180  LOAD_CONST               None
              182  YIELD_FROM       
          184_186  SETUP_ASYNC_WITH    526  'to 526'
              188  STORE_FAST               'r'

 L. 198       190  LOAD_FAST                'r'
              192  LOAD_ATTR                text
              194  LOAD_STR                 'utf-8'
              196  LOAD_CONST               ('encoding',)
              198  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              200  GET_AWAITABLE    
              202  LOAD_CONST               None
              204  YIELD_FROM       
              206  JUMP_IF_TRUE_OR_POP   210  'to 210'
              208  LOAD_CONST               None
            210_0  COME_FROM           206  '206'
              210  STORE_FAST               'response'

 L. 199       212  LOAD_FAST                'r'
              214  LOAD_ATTR                headers
              216  LOAD_STR                 'Content-Type'
              218  BINARY_SUBSCR    
              220  LOAD_STR                 'application/json'
              222  COMPARE_OP               ==
              224  POP_JUMP_IF_FALSE   236  'to 236'

 L. 200       226  LOAD_GLOBAL              json
              228  LOAD_METHOD              loads
              230  LOAD_FAST                'response'
              232  CALL_METHOD_1         1  ''
              234  STORE_FAST               'response'
            236_0  COME_FROM           224  '224'

 L. 203       236  LOAD_FAST                'r'
              238  LOAD_ATTR                headers
              240  LOAD_METHOD              get
              242  LOAD_STR                 'X-Ratelimit-Remaining'
              244  CALL_METHOD_1         1  ''
              246  STORE_FAST               'remaining'

 L. 204       248  LOAD_FAST                'remaining'
              250  LOAD_STR                 '0'
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   296  'to 296'
              258  LOAD_FAST                'r'
              260  LOAD_ATTR                status
              262  LOAD_CONST               429
              264  COMPARE_OP               !=
          266_268  POP_JUMP_IF_FALSE   296  'to 296'

 L. 205       270  LOAD_GLOBAL              utils
              272  LOAD_METHOD              _parse_ratelimit_header
              274  LOAD_FAST                'r'
              276  CALL_METHOD_1         1  ''
              278  STORE_FAST               'delta'

 L. 206       280  LOAD_GLOBAL              asyncio
              282  LOAD_METHOD              sleep
              284  LOAD_FAST                'delta'
              286  CALL_METHOD_1         1  ''
              288  GET_AWAITABLE    
              290  LOAD_CONST               None
              292  YIELD_FROM       
              294  POP_TOP          
            296_0  COME_FROM           266  '266'
            296_1  COME_FROM           254  '254'

 L. 208       296  LOAD_CONST               300
              298  LOAD_FAST                'r'
              300  LOAD_ATTR                status
              302  DUP_TOP          
              304  ROT_THREE        
              306  COMPARE_OP               >
          308_310  POP_JUMP_IF_FALSE   322  'to 322'
              312  LOAD_CONST               200
              314  COMPARE_OP               >=
          316_318  POP_JUMP_IF_FALSE   352  'to 352'
              320  JUMP_FORWARD        326  'to 326'
            322_0  COME_FROM           308  '308'
              322  POP_TOP          
              324  JUMP_FORWARD        352  'to 352'
            326_0  COME_FROM           320  '320'

 L. 209       326  LOAD_FAST                'response'
              328  POP_BLOCK        
              330  ROT_TWO          
              332  BEGIN_FINALLY    
              334  WITH_CLEANUP_START
              336  GET_AWAITABLE    
              338  LOAD_CONST               None
              340  YIELD_FROM       
              342  WITH_CLEANUP_FINISH
              344  POP_FINALLY           0  ''
              346  ROT_TWO          
              348  POP_TOP          
              350  RETURN_VALUE     
            352_0  COME_FROM           324  '324'
            352_1  COME_FROM           316  '316'

 L. 212       352  LOAD_FAST                'r'
              354  LOAD_ATTR                status
              356  LOAD_CONST               429
              358  COMPARE_OP               ==
          360_362  POP_JUMP_IF_FALSE   410  'to 410'

 L. 213       364  LOAD_FAST                'response'
              366  LOAD_STR                 'retry_after'
              368  BINARY_SUBSCR    
              370  LOAD_CONST               1000.0
              372  BINARY_TRUE_DIVIDE
              374  STORE_FAST               'retry_after'

 L. 214       376  LOAD_GLOBAL              asyncio
              378  LOAD_METHOD              sleep
              380  LOAD_FAST                'retry_after'
              382  CALL_METHOD_1         1  ''
              384  GET_AWAITABLE    
              386  LOAD_CONST               None
              388  YIELD_FROM       
              390  POP_TOP          

 L. 215       392  POP_BLOCK        
              394  BEGIN_FINALLY    
              396  WITH_CLEANUP_START
              398  GET_AWAITABLE    
              400  LOAD_CONST               None
              402  YIELD_FROM       
              404  WITH_CLEANUP_FINISH
              406  POP_FINALLY           0  ''
              408  JUMP_BACK           130  'to 130'
            410_0  COME_FROM           360  '360'

 L. 217       410  LOAD_FAST                'r'
              412  LOAD_ATTR                status
              414  LOAD_CONST               (500, 502)
              416  COMPARE_OP               in
          418_420  POP_JUMP_IF_FALSE   464  'to 464'

 L. 218       422  LOAD_GLOBAL              asyncio
              424  LOAD_METHOD              sleep
              426  LOAD_CONST               1
              428  LOAD_FAST                'tries'
              430  LOAD_CONST               2
              432  BINARY_MULTIPLY  
              434  BINARY_ADD       
              436  CALL_METHOD_1         1  ''
              438  GET_AWAITABLE    
              440  LOAD_CONST               None
              442  YIELD_FROM       
              444  POP_TOP          

 L. 219       446  POP_BLOCK        
              448  BEGIN_FINALLY    
              450  WITH_CLEANUP_START
              452  GET_AWAITABLE    
              454  LOAD_CONST               None
              456  YIELD_FROM       
              458  WITH_CLEANUP_FINISH
              460  POP_FINALLY           0  ''
              462  JUMP_BACK           130  'to 130'
            464_0  COME_FROM           418  '418'

 L. 221       464  LOAD_FAST                'r'
              466  LOAD_ATTR                status
              468  LOAD_CONST               403
              470  COMPARE_OP               ==
          472_474  POP_JUMP_IF_FALSE   488  'to 488'

 L. 222       476  LOAD_GLOBAL              Forbidden
              478  LOAD_FAST                'r'
              480  LOAD_FAST                'response'
              482  CALL_FUNCTION_2       2  ''
              484  RAISE_VARARGS_1       1  'exception instance'
              486  JUMP_FORWARD        522  'to 522'
            488_0  COME_FROM           472  '472'

 L. 223       488  LOAD_FAST                'r'
              490  LOAD_ATTR                status
              492  LOAD_CONST               404
              494  COMPARE_OP               ==
          496_498  POP_JUMP_IF_FALSE   512  'to 512'

 L. 224       500  LOAD_GLOBAL              NotFound
              502  LOAD_FAST                'r'
              504  LOAD_FAST                'response'
              506  CALL_FUNCTION_2       2  ''
              508  RAISE_VARARGS_1       1  'exception instance'
              510  JUMP_FORWARD        522  'to 522'
            512_0  COME_FROM           496  '496'

 L. 226       512  LOAD_GLOBAL              HTTPException
              514  LOAD_FAST                'r'
              516  LOAD_FAST                'response'
              518  CALL_FUNCTION_2       2  ''
              520  RAISE_VARARGS_1       1  'exception instance'
            522_0  COME_FROM           510  '510'
            522_1  COME_FROM           486  '486'
              522  POP_BLOCK        
              524  BEGIN_FINALLY    
            526_0  COME_FROM_ASYNC_WITH   184  '184'
              526  WITH_CLEANUP_START
              528  GET_AWAITABLE    
              530  LOAD_CONST               None
              532  YIELD_FROM       
              534  WITH_CLEANUP_FINISH
              536  END_FINALLY      
              538  JUMP_BACK           130  'to 130'
            540_0  COME_FROM           130  '130'

 L. 228       540  LOAD_GLOBAL              HTTPException
              542  LOAD_FAST                'r'
              544  LOAD_FAST                'response'
              546  CALL_FUNCTION_2       2  ''
              548  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `ROT_TWO' instruction at offset 330

    async def handle_execution_response(self, response, *, wait):
        data = await response
        if not wait:
            return data
        from .message import Message
        return Message(data=data, state=(self.webhook._state), channel=(self.webhook.channel))


class RequestsWebhookAdapter(WebhookAdapter):
    __doc__ = 'A webhook adapter suited for use with ``requests``.\n\n    Only versions of :doc:`req:index` higher than 2.13.0 are supported.\n\n    Parameters\n    -----------\n    session: Optional[`requests.Session <http://docs.python-requests.org/en/latest/api/#requests.Session>`_]\n        The requests session to use for sending requests. If not given then\n        each request will create a new session. Note if a session is given,\n        the webhook adapter **will not** clean it up for you. You must close\n        the session yourself.\n    sleep: :class:`bool`\n        Whether to sleep the thread when encountering a 429 or pre-emptive\n        rate limit or a 5xx status code. Defaults to ``True``. If set to\n        ``False`` then this will raise an :exc:`HTTPException` instead.\n    '

    def __init__(self, session=None, *, sleep=True):
        import requests
        self.session = session or requests
        self.sleep = sleep

    def request--- This code section failed: ---

 L. 263         0  BUILD_MAP_0           0 
                2  STORE_FAST               'headers'

 L. 264         4  LOAD_CONST               None
                6  STORE_FAST               'data'

 L. 265         8  LOAD_FAST                'files'
               10  JUMP_IF_TRUE_OR_POP    14  'to 14'
               12  BUILD_LIST_0          0 
             14_0  COME_FROM            10  '10'
               14  STORE_FAST               'files'

 L. 266        16  LOAD_FAST                'payload'
               18  POP_JUMP_IF_FALSE    38  'to 38'

 L. 267        20  LOAD_STR                 'application/json'
               22  LOAD_FAST                'headers'
               24  LOAD_STR                 'Content-Type'
               26  STORE_SUBSCR     

 L. 268        28  LOAD_GLOBAL              utils
               30  LOAD_METHOD              to_json
               32  LOAD_FAST                'payload'
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'data'
             38_0  COME_FROM            18  '18'

 L. 270        38  LOAD_FAST                'multipart'
               40  LOAD_CONST               None
               42  COMPARE_OP               is-not
               44  POP_JUMP_IF_FALSE    60  'to 60'

 L. 271        46  LOAD_STR                 'payload_json'
               48  LOAD_FAST                'multipart'
               50  LOAD_METHOD              pop
               52  LOAD_STR                 'payload_json'
               54  CALL_METHOD_1         1  ''
               56  BUILD_MAP_1           1 
               58  STORE_FAST               'data'
             60_0  COME_FROM            44  '44'

 L. 273        60  LOAD_GLOBAL              range
               62  LOAD_CONST               5
               64  CALL_FUNCTION_1       1  ''
               66  GET_ITER         
             68_0  COME_FROM           412  '412'
             68_1  COME_FROM           400  '400'
             68_2  COME_FROM           376  '376'
             68_3  COME_FROM           352  '352'
             68_4  COME_FROM           300  '300'
            68_70  FOR_ITER            414  'to 414'
               72  STORE_FAST               'tries'

 L. 274        74  LOAD_FAST                'files'
               76  GET_ITER         
             78_0  COME_FROM            94  '94'
               78  FOR_ITER             96  'to 96'
               80  STORE_FAST               'file'

 L. 275        82  LOAD_FAST                'file'
               84  LOAD_ATTR                reset
               86  LOAD_FAST                'tries'
               88  LOAD_CONST               ('seek',)
               90  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               92  POP_TOP          
               94  JUMP_BACK            78  'to 78'
             96_0  COME_FROM            78  '78'

 L. 277        96  LOAD_FAST                'self'
               98  LOAD_ATTR                session
              100  LOAD_ATTR                request
              102  LOAD_FAST                'verb'
              104  LOAD_FAST                'url'
              106  LOAD_FAST                'headers'
              108  LOAD_FAST                'data'
              110  LOAD_FAST                'multipart'
              112  LOAD_CONST               ('headers', 'data', 'files')
              114  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              116  STORE_FAST               'r'

 L. 278       118  LOAD_STR                 'utf-8'
              120  LOAD_FAST                'r'
              122  STORE_ATTR               encoding

 L. 280       124  LOAD_FAST                'r'
              126  LOAD_ATTR                text
              128  JUMP_IF_TRUE_OR_POP   132  'to 132'
              130  LOAD_CONST               None
            132_0  COME_FROM           128  '128'
              132  STORE_FAST               'response'

 L. 283       134  LOAD_FAST                'r'
              136  LOAD_ATTR                status_code
              138  LOAD_FAST                'r'
              140  STORE_ATTR               status

 L. 285       142  LOAD_FAST                'r'
              144  LOAD_ATTR                headers
              146  LOAD_STR                 'Content-Type'
              148  BINARY_SUBSCR    
              150  LOAD_STR                 'application/json'
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   166  'to 166'

 L. 286       156  LOAD_GLOBAL              json
              158  LOAD_METHOD              loads
              160  LOAD_FAST                'response'
              162  CALL_METHOD_1         1  ''
              164  STORE_FAST               'response'
            166_0  COME_FROM           154  '154'

 L. 289       166  LOAD_FAST                'r'
              168  LOAD_ATTR                headers
              170  LOAD_METHOD              get
              172  LOAD_STR                 'X-Ratelimit-Remaining'
              174  CALL_METHOD_1         1  ''
              176  STORE_FAST               'remaining'

 L. 290       178  LOAD_FAST                'remaining'
              180  LOAD_STR                 '0'
              182  COMPARE_OP               ==
              184  POP_JUMP_IF_FALSE   222  'to 222'
              186  LOAD_FAST                'r'
              188  LOAD_ATTR                status
              190  LOAD_CONST               429
              192  COMPARE_OP               !=
              194  POP_JUMP_IF_FALSE   222  'to 222'
              196  LOAD_FAST                'self'
              198  LOAD_ATTR                sleep
              200  POP_JUMP_IF_FALSE   222  'to 222'

 L. 291       202  LOAD_GLOBAL              utils
              204  LOAD_METHOD              _parse_ratelimit_header
              206  LOAD_FAST                'r'
              208  CALL_METHOD_1         1  ''
              210  STORE_FAST               'delta'

 L. 292       212  LOAD_GLOBAL              time
              214  LOAD_METHOD              sleep
              216  LOAD_FAST                'delta'
              218  CALL_METHOD_1         1  ''
              220  POP_TOP          
            222_0  COME_FROM           200  '200'
            222_1  COME_FROM           194  '194'
            222_2  COME_FROM           184  '184'

 L. 294       222  LOAD_CONST               300
              224  LOAD_FAST                'r'
              226  LOAD_ATTR                status
              228  DUP_TOP          
              230  ROT_THREE        
              232  COMPARE_OP               >
              234  POP_JUMP_IF_FALSE   246  'to 246'
              236  LOAD_CONST               200
              238  COMPARE_OP               >=
          240_242  POP_JUMP_IF_FALSE   258  'to 258'
              244  JUMP_FORWARD        250  'to 250'
            246_0  COME_FROM           234  '234'
              246  POP_TOP          
              248  JUMP_FORWARD        258  'to 258'
            250_0  COME_FROM           244  '244'

 L. 295       250  LOAD_FAST                'response'
              252  ROT_TWO          
              254  POP_TOP          
              256  RETURN_VALUE     
            258_0  COME_FROM           248  '248'
            258_1  COME_FROM           240  '240'

 L. 298       258  LOAD_FAST                'r'
              260  LOAD_ATTR                status
              262  LOAD_CONST               429
              264  COMPARE_OP               ==
          266_268  POP_JUMP_IF_FALSE   314  'to 314'

 L. 299       270  LOAD_FAST                'self'
              272  LOAD_ATTR                sleep
          274_276  POP_JUMP_IF_FALSE   304  'to 304'

 L. 300       278  LOAD_FAST                'response'
              280  LOAD_STR                 'retry_after'
              282  BINARY_SUBSCR    
              284  LOAD_CONST               1000.0
              286  BINARY_TRUE_DIVIDE
              288  STORE_FAST               'retry_after'

 L. 301       290  LOAD_GLOBAL              time
              292  LOAD_METHOD              sleep
              294  LOAD_FAST                'retry_after'
              296  CALL_METHOD_1         1  ''
              298  POP_TOP          

 L. 302       300  JUMP_BACK            68  'to 68'
              302  JUMP_FORWARD        314  'to 314'
            304_0  COME_FROM           274  '274'

 L. 304       304  LOAD_GLOBAL              HTTPException
              306  LOAD_FAST                'r'
              308  LOAD_FAST                'response'
              310  CALL_FUNCTION_2       2  ''
              312  RAISE_VARARGS_1       1  'exception instance'
            314_0  COME_FROM           302  '302'
            314_1  COME_FROM           266  '266'

 L. 306       314  LOAD_FAST                'self'
              316  LOAD_ATTR                sleep
          318_320  POP_JUMP_IF_FALSE   354  'to 354'
              322  LOAD_FAST                'r'
              324  LOAD_ATTR                status
              326  LOAD_CONST               (500, 502)
              328  COMPARE_OP               in
          330_332  POP_JUMP_IF_FALSE   354  'to 354'

 L. 307       334  LOAD_GLOBAL              time
              336  LOAD_METHOD              sleep
              338  LOAD_CONST               1
              340  LOAD_FAST                'tries'
              342  LOAD_CONST               2
              344  BINARY_MULTIPLY  
              346  BINARY_ADD       
              348  CALL_METHOD_1         1  ''
              350  POP_TOP          

 L. 308       352  JUMP_BACK            68  'to 68'
            354_0  COME_FROM           330  '330'
            354_1  COME_FROM           318  '318'

 L. 310       354  LOAD_FAST                'r'
              356  LOAD_ATTR                status
              358  LOAD_CONST               403
              360  COMPARE_OP               ==
          362_364  POP_JUMP_IF_FALSE   378  'to 378'

 L. 311       366  LOAD_GLOBAL              Forbidden
              368  LOAD_FAST                'r'
              370  LOAD_FAST                'response'
              372  CALL_FUNCTION_2       2  ''
              374  RAISE_VARARGS_1       1  'exception instance'
              376  JUMP_BACK            68  'to 68'
            378_0  COME_FROM           362  '362'

 L. 312       378  LOAD_FAST                'r'
              380  LOAD_ATTR                status
              382  LOAD_CONST               404
              384  COMPARE_OP               ==
          386_388  POP_JUMP_IF_FALSE   402  'to 402'

 L. 313       390  LOAD_GLOBAL              NotFound
              392  LOAD_FAST                'r'
              394  LOAD_FAST                'response'
              396  CALL_FUNCTION_2       2  ''
              398  RAISE_VARARGS_1       1  'exception instance'
              400  JUMP_BACK            68  'to 68'
            402_0  COME_FROM           386  '386'

 L. 315       402  LOAD_GLOBAL              HTTPException
              404  LOAD_FAST                'r'
              406  LOAD_FAST                'response'
              408  CALL_FUNCTION_2       2  ''
              410  RAISE_VARARGS_1       1  'exception instance'
              412  JUMP_BACK            68  'to 68'
            414_0  COME_FROM            68  '68'

 L. 317       414  LOAD_GLOBAL              HTTPException
              416  LOAD_FAST                'r'
              418  LOAD_FAST                'response'
              420  CALL_FUNCTION_2       2  ''
              422  RAISE_VARARGS_1       1  'exception instance'

Parse error at or near `CALL_FUNCTION_2' instruction at offset 420

    def handle_execution_response(self, response, *, wait):
        if not wait:
            return response
        from .message import Message
        return Message(data=response, state=(self.webhook._state), channel=(self.webhook.channel))


class _FriendlyHttpAttributeErrorHelper:
    __slots__ = ()

    def __getattr__(self, attr):
        raise AttributeError('PartialWebhookState does not support http methods.')


class _PartialWebhookState:
    __slots__ = ('loop', )

    def __init__(self, adapter):
        try:
            self.loop = adapter.loop
        except AttributeError:
            self.loop = None

    def _get_guild(self, guild_id):
        pass

    def store_user(self, data):
        return BaseUser(state=self, data=data)

    @property
    def is_bot(self):
        return True

    @property
    def http(self):
        return _FriendlyHttpAttributeErrorHelper()

    def __getattr__(self, attr):
        raise AttributeError('PartialWebhookState does not support {0!r}.'.format(attr))


class Webhook:
    __doc__ = "Represents a Discord webhook.\n\n    Webhooks are a form to send messages to channels in Discord without a\n    bot user or authentication.\n\n    There are two main ways to use Webhooks. The first is through the ones\n    received by the library such as :meth:`.Guild.webhooks` and\n    :meth:`.TextChannel.webhooks`. The ones received by the library will\n    automatically have an adapter bound using the library's HTTP session.\n    Those webhooks will have :meth:`~.Webhook.send`, :meth:`~.Webhook.delete` and\n    :meth:`~.Webhook.edit` as coroutines.\n\n    The second form involves creating a webhook object manually without having\n    it bound to a websocket connection using the :meth:`~.Webhook.from_url` or\n    :meth:`~.Webhook.partial` classmethods. This form allows finer grained control\n    over how requests are done, allowing you to mix async and sync code using either\n    :doc:`aiohttp <aio:index>` or :doc:`req:index`.\n\n    For example, creating a webhook from a URL and using :doc:`aiohttp <aio:index>`:\n\n    .. code-block:: python3\n\n        from discord import Webhook, AsyncWebhookAdapter\n        import aiohttp\n\n        async def foo():\n            async with aiohttp.ClientSession() as session:\n                webhook = Webhook.from_url('url-here', adapter=AsyncWebhookAdapter(session))\n                await webhook.send('Hello World', username='Foo')\n\n    Or creating a webhook from an ID and token and using :doc:`req:index`:\n\n    .. code-block:: python3\n\n        import requests\n        from discord import Webhook, RequestsWebhookAdapter\n\n        webhook = Webhook.partial(123456, 'abcdefg', adapter=RequestsWebhookAdapter())\n        webhook.send('Hello World', username='Foo')\n\n    Attributes\n    ------------\n    id: :class:`int`\n        The webhook's ID\n    type: :class:`WebhookType`\n        The type of the webhook.\n\n        .. versionadded:: 1.3\n\n    token: Optional[:class:`str`]\n        The authentication token of the webhook. If this is ``None``\n        then the webhook cannot be used to make requests.\n    guild_id: Optional[:class:`int`]\n        The guild ID this webhook is for.\n    channel_id: Optional[:class:`int`]\n        The channel ID this webhook is for.\n    user: Optional[:class:`abc.User`]\n        The user this webhook was created by. If the webhook was\n        received without authentication then this will be ``None``.\n    name: Optional[:class:`str`]\n        The default name of the webhook.\n    avatar: Optional[:class:`str`]\n        The default avatar of the webhook.\n    "
    __slots__ = ('id', 'type', 'guild_id', 'channel_id', 'user', 'name', 'avatar',
                 'token', '_state', '_adapter')

    def __init__(self, data, *, adapter, state=None):
        self.id = int(data['id'])
        self.type = try_enum(WebhookType, int(data['type']))
        self.channel_id = utils._get_as_snowflake(data, 'channel_id')
        self.guild_id = utils._get_as_snowflake(data, 'guild_id')
        self.name = data.get('name')
        self.avatar = data.get('avatar')
        self.token = data.get('token')
        self._state = state or _PartialWebhookState(adapter)
        self._adapter = adapter
        self._adapter._prepare(self)
        user = data.get('user')
        if user is None:
            self.user = None
        elif state is None:
            self.user = BaseUser(state=None, data=user)
        else:
            self.user = User(state=state, data=user)

    def __repr__(self):
        return '<Webhook id=%r>' % self.id

    @property
    def url(self):
        """Returns the webhook's url."""
        return 'https://discordapp.com/api/webhooks/{}/{}'.format(self.id, self.token)

    @classmethod
    def partial(cls, id, token, *, adapter):
        """Creates a partial :class:`Webhook`.

        A partial webhook is just a webhook object with an ID and a token.

        Parameters
        -----------
        id: :class:`int`
            The ID of the webhook.
        token: :class:`str`
            The authentication token of the webhook.
        adapter: :class:`WebhookAdapter`
            The webhook adapter to use when sending requests. This is
            typically :class:`AsyncWebhookAdapter` for :doc:`aiohttp <aio:index>` or
            :class:`RequestsWebhookAdapter` for :doc:`req:index`.
        """
        if not isinstance(adapter, WebhookAdapter):
            raise TypeError('adapter must be a subclass of WebhookAdapter')
        data = {'id':id, 
         'type':1, 
         'token':token}
        return cls(data, adapter=adapter)

    @classmethod
    def from_url(cls, url, *, adapter):
        """Creates a partial :class:`Webhook` from a webhook URL.

        Parameters
        ------------
        url: :class:`str`
            The URL of the webhook.
        adapter: :class:`WebhookAdapter`
            The webhook adapter to use when sending requests. This is
            typically :class:`AsyncWebhookAdapter` for :doc:`aiohttp <aio:index>` or
            :class:`RequestsWebhookAdapter` for :doc:`req:index`.

        Raises
        -------
        InvalidArgument
            The URL is invalid.
        """
        m = re.search('discordapp.com/api/webhooks/(?P<id>[0-9]{17,21})/(?P<token>[A-Za-z0-9\\.\\-\\_]{60,68})', url)
        if m is None:
            raise InvalidArgument('Invalid webhook URL given.')
        data = m.groupdict()
        data['type'] = 1
        return cls(data, adapter=adapter)

    @classmethod
    def _as_follower(cls, data, *, channel, user):
        name = '{} #{}'.format(channel.guild, channel)
        feed = {'id':data['webhook_id'], 
         'type':2, 
         'name':name, 
         'channel_id':channel.id, 
         'guild_id':channel.guild.id, 
         'user':{'username':user.name, 
          'discriminator':user.discriminator, 
          'id':user.id, 
          'avatar':user.avatar}}
        session = channel._state.http._HTTPClient__session
        return cls(feed, adapter=AsyncWebhookAdapter(session=session))

    @classmethod
    def from_state(cls, data, state):
        session = state.http._HTTPClient__session
        return cls(data, adapter=AsyncWebhookAdapter(session=session), state=state)

    @property
    def guild(self):
        """Optional[:class:`Guild`]: The guild this webhook belongs to.

        If this is a partial webhook, then this will always return ``None``.
        """
        return self._state._get_guild(self.guild_id)

    @property
    def channel(self):
        """Optional[:class:`TextChannel`]: The text channel this webhook belongs to.

        If this is a partial webhook, then this will always return ``None``.
        """
        guild = self.guild
        return guild and guild.get_channel(self.channel_id)

    @property
    def created_at(self):
        """:class:`datetime.datetime`: Returns the webhook's creation time in UTC."""
        return utils.snowflake_time(self.id)

    @property
    def avatar_url(self):
        """Returns an :class:`Asset` for the avatar the webhook has.

        If the webhook does not have a traditional avatar, an asset for
        the default avatar is returned instead.

        This is equivalent to calling :meth:`avatar_url_as` with the
        default parameters.
        """
        return self.avatar_url_as()

    def avatar_url_as(self, *, format=None, size=1024):
        """Returns an :class:`Asset` for the avatar the webhook has.

        If the webhook does not have a traditional avatar, an asset for
        the default avatar is returned instead.

        The format must be one of 'jpeg', 'jpg', or 'png'.
        The size must be a power of 2 between 16 and 1024.

        Parameters
        -----------
        format: Optional[:class:`str`]
            The format to attempt to convert the avatar to.
            If the format is ``None``, then it is equivalent to png.
        size: :class:`int`
            The size of the image to display.

        Raises
        ------
        InvalidArgument
            Bad image format passed to ``format`` or invalid ``size``.

        Returns
        --------
        :class:`Asset`
            The resulting CDN asset.
        """
        if self.avatar is None:
            return Asset(self._state, '/embed/avatars/0.png')
        if not utils.valid_icon_size(size):
            raise InvalidArgument('size must be a power of 2 between 16 and 1024')
        format = format or 'png'
        if format not in ('png', 'jpg', 'jpeg'):
            raise InvalidArgument("format must be one of 'png', 'jpg', or 'jpeg'.")
        url = '/avatars/{0.id}/{0.avatar}.{1}?size={2}'.format(self, format, size)
        return Asset(self._state, url)

    def delete(self):
        """|maybecoro|

        Deletes this Webhook.

        If the webhook is constructed with a :class:`RequestsWebhookAdapter` then this is
        not a coroutine.

        Raises
        -------
        HTTPException
            Deleting the webhook failed.
        NotFound
            This webhook does not exist.
        Forbidden
            You do not have permissions to delete this webhook.
        InvalidArgument
            This webhook does not have a token associated with it.
        """
        if self.token is None:
            raise InvalidArgument('This webhook does not have a token associated with it')
        return self._adapter.delete_webhook()

    def edit(self, **kwargs):
        """|maybecoro|

        Edits this Webhook.

        If the webhook is constructed with a :class:`RequestsWebhookAdapter` then this is
        not a coroutine.

        Parameters
        -------------
        name: Optional[:class:`str`]
            The webhook's new default name.
        avatar: Optional[:class:`bytes`]
            A :term:`py:bytes-like object` representing the webhook's new default avatar.

        Raises
        -------
        HTTPException
            Editing the webhook failed.
        NotFound
            This webhook does not exist.
        InvalidArgument
            This webhook does not have a token associated with it.
        """
        if self.token is None:
            raise InvalidArgument('This webhook does not have a token associated with it')
        payload = {}
        try:
            name = kwargs['name']
        except KeyError:
            pass
        else:
            if name is not None:
                payload['name'] = str(name)
            else:
                payload['name'] = None
        try:
            avatar = kwargs['avatar']
        except KeyError:
            pass
        else:
            if avatar is not None:
                payload['avatar'] = utils._bytes_to_base64_data(avatar)
            else:
                payload['avatar'] = None
        return (self._adapter.edit_webhook)(**payload)

    def send(self, content=None, *, wait=False, username=None, avatar_url=None, tts=False, file=None, files=None, embed=None, embeds=None):
        """|maybecoro|

        Sends a message using the webhook.

        If the webhook is constructed with a :class:`RequestsWebhookAdapter` then this is
        not a coroutine.

        The content must be a type that can convert to a string through ``str(content)``.

        To upload a single file, the ``file`` parameter should be used with a
        single :class:`File` object.

        If the ``embed`` parameter is provided, it must be of type :class:`Embed` and
        it must be a rich embed type. You cannot mix the ``embed`` parameter with the
        ``embeds`` parameter, which must be a :class:`list` of :class:`Embed` objects to send.

        Parameters
        ------------
        content: :class:`str`
            The content of the message to send.
        wait: :class:`bool`
            Whether the server should wait before sending a response. This essentially
            means that the return type of this function changes from ``None`` to
            a :class:`Message` if set to ``True``.
        username: :class:`str`
            The username to send with this message. If no username is provided
            then the default username for the webhook is used.
        avatar_url: Union[:class:`str`, :class:`Asset`]
            The avatar URL to send with this message. If no avatar URL is provided
            then the default avatar for the webhook is used.
        tts: :class:`bool`
            Indicates if the message should be sent using text-to-speech.
        file: :class:`File`
            The file to upload. This cannot be mixed with ``files`` parameter.
        files: List[:class:`File`]
            A list of files to send with the content. This cannot be mixed with the
            ``file`` parameter.
        embed: :class:`Embed`
            The rich embed for the content to send. This cannot be mixed with
            ``embeds`` parameter.
        embeds: List[:class:`Embed`]
            A list of embeds to send with the content. Maximum of 10. This cannot
            be mixed with the ``embed`` parameter.

        Raises
        --------
        HTTPException
            Sending the message failed.
        NotFound
            This webhook was not found.
        Forbidden
            The authorization token for the webhook is incorrect.
        InvalidArgument
            You specified both ``embed`` and ``embeds`` or the length of
            ``embeds`` was invalid or there was no token associated with
            this webhook.

        Returns
        ---------
        Optional[:class:`Message`]
            The message that was sent.
        """
        payload = {}
        if self.token is None:
            raise InvalidArgument('This webhook does not have a token associated with it')
        if files is not None:
            if file is not None:
                raise InvalidArgument('Cannot mix file and files keyword arguments.')
        if embeds is not None:
            if embed is not None:
                raise InvalidArgument('Cannot mix embed and embeds keyword arguments.')
        if embeds is not None:
            if len(embeds) > 10:
                raise InvalidArgument('embeds has a maximum of 10 elements.')
            payload['embeds'] = [e.to_dict() for e in embeds]
        if embed is not None:
            payload['embeds'] = [
             embed.to_dict()]
        if content is not None:
            payload['content'] = str(content)
        payload['tts'] = tts
        if avatar_url:
            payload['avatar_url'] = str(avatar_url)
        if username:
            payload['username'] = username
        return self._adapter.execute_webhook(wait=wait, file=file, files=files, payload=payload)

    def execute(self, *args, **kwargs):
        """An alias for :meth:`~.Webhook.send`."""
        return (self.send)(*args, **kwargs)