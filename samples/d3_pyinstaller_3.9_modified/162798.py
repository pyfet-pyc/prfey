# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: telebot\__init__.py
from __future__ import print_function
from datetime import datetime
import logging, re, sys, threading, time, traceback
from typing import Any, Callable, List, Optional, Union
import telebot.util, telebot.types
logger = logging.getLogger('TeleBot')
formatter = logging.Formatter('%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: "%(message)s"')
console_output_handler = logging.StreamHandler(sys.stderr)
console_output_handler.setFormatter(formatter)
logger.addHandler(console_output_handler)
logger.setLevel(logging.ERROR)
from telebot import apihelper, util, types
from telebot.handler_backends import MemoryHandlerBackend, FileHandlerBackend
REPLY_MARKUP_TYPES = Union[(
 types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup,
 types.ReplyKeyboardRemove, types.ForceReply)]

class Handler:
    __doc__ = '\n    Class for (next step|reply) handlers\n    '

    def __init__(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def __getitem__(self, item):
        return getattr(self, item)


class ExceptionHandler:
    __doc__ = '\n    Class for handling exceptions while Polling\n    '

    def handle(self, exception):
        return False


class TeleBot:
    __doc__ = ' This is TeleBot Class\n    Methods:\n        getMe\n        logOut\n        close\n        sendMessage\n        forwardMessage\n        copyMessage\n        deleteMessage\n        sendPhoto\n        sendAudio\n        sendDocument\n        sendSticker\n        sendVideo\n        sendVenue\n        sendAnimation\n        sendVideoNote\n        sendLocation\n        sendChatAction\n        sendDice\n        sendContact\n        sendInvoice\n        sendMediaGroup\n        getUserProfilePhotos\n        getUpdates\n        getFile\n        sendPoll\n        stopPoll\n        sendGame\n        setGameScore\n        getGameHighScores\n        editMessageText\n        editMessageCaption\n        editMessageMedia\n        editMessageReplyMarkup\n        editMessageLiveLocation\n        stopMessageLiveLocation\n        kickChatMember\n        unbanChatMember\n        restrictChatMember\n        promoteChatMember\n        setChatAdministratorCustomTitle\n        setChatPermissions\n        createChatInviteLink\n        editChatInviteLink\n        revokeChatInviteLink\n        exportChatInviteLink\n        setChatStickerSet\n        deleteChatStickerSet\n        createNewStickerSet\n        addStickerToSet\n        deleteStickerFromSet\n        setStickerPositionInSet\n        uploadStickerFile\n        setStickerSetThumb\n        getStickerSet\n        setChatPhoto\n        deleteChatPhoto\n        setChatTitle\n        setChatDescription\n        pinChatMessage\n        unpinChatMessage\n        leaveChat\n        getChat\n        getChatAdministrators\n        getChatMembersCount\n        getChatMember\n        answerCallbackQuery\n        getMyCommands\n        setMyCommands\n        answerInlineQuery\n        answerShippingQuery\n        answerPreCheckoutQuery\n        '

    def __init__(self, token, parse_mode=None, threaded=True, skip_pending=False, num_threads=2, next_step_backend=None, reply_backend=None, exception_handler=None, last_update_id=0, suppress_middleware_excepions=False):
        """
        :param token: bot API token
        :param parse_mode: default parse_mode
        :return: Telebot object.
        """
        self.token = token
        self.parse_mode = parse_mode
        self.update_listener = []
        self.skip_pending = skip_pending
        self.suppress_middleware_excepions = suppress_middleware_excepions
        self._TeleBot__stop_polling = threading.Event()
        self.last_update_id = last_update_id
        self.exc_info = None
        self.next_step_backend = next_step_backend
        if not self.next_step_backend:
            self.next_step_backend = MemoryHandlerBackend()
        self.reply_backend = reply_backend
        if not self.reply_backend:
            self.reply_backend = MemoryHandlerBackend()
        self.exception_handler = exception_handler
        self.message_handlers = []
        self.edited_message_handlers = []
        self.channel_post_handlers = []
        self.edited_channel_post_handlers = []
        self.inline_handlers = []
        self.chosen_inline_handlers = []
        self.callback_query_handlers = []
        self.shipping_query_handlers = []
        self.pre_checkout_query_handlers = []
        self.poll_handlers = []
        self.poll_answer_handlers = []
        self.my_chat_member_handlers = []
        self.chat_member_handlers = []
        if apihelper.ENABLE_MIDDLEWARE:
            self.typed_middleware_handlers = {'message':[],  'edited_message':[],  'channel_post':[],  'edited_channel_post':[],  'inline_query':[],  'chosen_inline_result':[],  'callback_query':[],  'shipping_query':[],  'pre_checkout_query':[],  'poll':[],  'poll_answer':[],  'my_chat_member':[],  'chat_member':[]}
            self.default_middleware_handlers = []
        self.threaded = threaded
        if self.threaded:
            self.worker_pool = util.ThreadPool(num_threads=num_threads)

    def enable_save_next_step_handlers(self, delay=120, filename='./.handler-saves/step.save'):
        """
        Enable saving next step handlers (by default saving disabled)

        This function explicitly assigns FileHandlerBackend (instead of Saver) just to keep backward
        compatibility whose purpose was to enable file saving capability for handlers. And the same
        implementation is now available with FileHandlerBackend

        Most probably this function should be deprecated in future major releases

        :param delay: Delay between changes in handlers and saving
        :param filename: Filename of save file
        """
        self.next_step_backend = FileHandlerBackend(self.next_step_backend.handlers, filename, delay)

    def enable_save_reply_handlers(self, delay=120, filename='./.handler-saves/reply.save'):
        """
        Enable saving reply handlers (by default saving disable)

        This function explicitly assigns FileHandlerBackend (instead of Saver) just to keep backward
        compatibility whose purpose was to enable file saving capability for handlers. And the same
        implementation is now available with FileHandlerBackend

        Most probably this function should be deprecated in future major releases

        :param delay: Delay between changes in handlers and saving
        :param filename: Filename of save file
        """
        self.reply_backend = FileHandlerBackend(self.reply_backend.handlers, filename, delay)

    def disable_save_next_step_handlers(self):
        """
        Disable saving next step handlers (by default saving disable)

        This function is left to keep backward compatibility whose purpose was to disable file saving capability
        for handlers. For the same purpose, MemoryHandlerBackend is reassigned as a new next_step_backend backend
        instead of FileHandlerBackend.

        Most probably this function should be deprecated in future major releases
        """
        self.next_step_backend = MemoryHandlerBackend(self.next_step_backend.handlers)

    def disable_save_reply_handlers(self):
        """
        Disable saving next step handlers (by default saving disable)

        This function is left to keep backward compatibility whose purpose was to disable file saving capability
        for handlers. For the same purpose, MemoryHandlerBackend is reassigned as a new reply_backend backend
        instead of FileHandlerBackend.

        Most probably this function should be deprecated in future major releases
        """
        self.reply_backend = MemoryHandlerBackend(self.reply_backend.handlers)

    def load_next_step_handlers(self, filename='./.handler-saves/step.save', del_file_after_loading=True):
        """
        Load next step handlers from save file

        This function is left to keep backward compatibility whose purpose was to load handlers from file with the
        help of FileHandlerBackend and is only recommended to use if next_step_backend was assigned as
        FileHandlerBackend before entering this function

        Most probably this function should be deprecated in future major releases

        :param filename: Filename of the file where handlers was saved
        :param del_file_after_loading: Is passed True, after loading save file will be deleted
        """
        self.next_step_backend.load_handlers(filename, del_file_after_loading)

    def load_reply_handlers(self, filename='./.handler-saves/reply.save', del_file_after_loading=True):
        """
        Load reply handlers from save file

        This function is left to keep backward compatibility whose purpose was to load handlers from file with the
        help of FileHandlerBackend and is only recommended to use if reply_backend was assigned as
        FileHandlerBackend before entering this function

        Most probably this function should be deprecated in future major releases

        :param filename: Filename of the file where handlers was saved
        :param del_file_after_loading: Is passed True, after loading save file will be deleted
        """
        self.reply_backend.load_handlers(filename, del_file_after_loading)

    def set_webhook(self, url=None, certificate=None, max_connections=None, allowed_updates=None, ip_address=None, drop_pending_updates=None, timeout=None):
        """
        Use this method to specify a url and receive incoming updates via an outgoing webhook. Whenever there is an
        update for the bot, we will send an HTTPS POST request to the specified url,
        containing a JSON-serialized Update.
        In case of an unsuccessful request, we will give up after a reasonable amount of attempts.
        Returns True on success.

        :param url: HTTPS url to send updates to. Use an empty string to remove webhook integration
        :param certificate: Upload your public key certificate so that the root certificate in use can be checked.
            See our self-signed guide for details.
        :param max_connections: Maximum allowed number of simultaneous HTTPS connections to the webhook
            for update delivery, 1-100. Defaults to 40. Use lower values to limit the load on your bot's server,
            and higher values to increase your bot's throughput.
        :param allowed_updates: A JSON-serialized list of the update types you want your bot to receive.
            For example, specify [“message”, “edited_channel_post”, “callback_query”] to only receive updates
            of these types. See Update for a complete list of available update types.
            Specify an empty list to receive all updates regardless of type (default).
            If not specified, the previous setting will be used.
        :param ip_address: The fixed IP address which will be used to send webhook requests instead of the IP address
            resolved through DNS
        :param drop_pending_updates: Pass True to drop all pending updates
        :param timeout: Integer. Request connection timeout
        :return:
        """
        return apihelper.set_webhook(self.token, url, certificate, max_connections, allowed_updates, ip_address, drop_pending_updates, timeout)

    def delete_webhook(self, drop_pending_updates=None, timeout=None):
        """
        Use this method to remove webhook integration if you decide to switch back to getUpdates.

        :param drop_pending_updates: Pass True to drop all pending updates
        :param timeout: Integer. Request connection timeout
        :return: bool
        """
        return apihelper.delete_webhook(self.token, drop_pending_updates, timeout)

    def get_webhook_info(self, timeout=None):
        """
        Use this method to get current webhook status. Requires no parameters.
        If the bot is using getUpdates, will return an object with the url field empty.

        :param timeout: Integer. Request connection timeout
        :return: On success, returns a WebhookInfo object.
        """
        result = apihelper.get_webhook_info(self.token, timeout)
        return types.WebhookInfo.de_json(result)

    def remove_webhook(self):
        return self.set_webhook()

    def get_updates(self, offset: Optional[int]=None, limit: Optional[int]=None, timeout: Optional[int]=20, allowed_updates: Optional[List[str]]=None, long_polling_timeout: int=20) -> List[types.Update]:
        """
        Use this method to receive incoming updates using long polling (wiki). An Array of Update objects is returned.
        :param allowed_updates: Array of string. List the types of updates you want your bot to receive.
        :param offset: Integer. Identifier of the first update to be returned.
        :param limit: Integer. Limits the number of updates to be retrieved.
        :param timeout: Integer. Request connection timeout
        :param long_polling_timeout. Timeout in seconds for long polling.
        :return: array of Updates
        """
        json_updates = apihelper.get_updates(self.token, offset, limit, timeout, allowed_updates, long_polling_timeout)
        ret = []
        for ju in json_updates:
            ret.append(types.Update.de_json(ju))
        else:
            return ret

    def __skip_updates(self):
        """
        Get and discard all pending updates before first poll of the bot
        :return: total updates skipped
        """
        total = 0
        updates = self.get_updates(offset=(self.last_update_id), long_polling_timeout=1)
        while True:
            if updates:
                total += len(updates)
                for update in updates:
                    if update.update_id > self.last_update_id:
                        self.last_update_id = update.update_id
                else:
                    updates = self.get_updates(offset=(self.last_update_id + 1), long_polling_timeout=1)

        return total

    def __retrieve_updates(self, timeout=20, long_polling_timeout=20, allowed_updates=None):
        """
        Retrieves any updates from the Telegram API.
        Registered listeners and applicable message handlers will be notified when a new message arrives.
        :raises ApiException when a call has failed.
        """
        if self.skip_pending:
            logger.debug('Skipped {0} pending messages'.format(self._TeleBot__skip_updates()))
            self.skip_pending = False
        updates = self.get_updates(offset=(self.last_update_id + 1), allowed_updates=allowed_updates,
          timeout=timeout,
          long_polling_timeout=long_polling_timeout)
        self.process_new_updates(updates)

    def process_new_updates--- This code section failed: ---

 L. 396         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'updates'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'upd_count'

 L. 397         8  LOAD_GLOBAL              logger
               10  LOAD_METHOD              debug
               12  LOAD_STR                 'Received {0} new updates'
               14  LOAD_METHOD              format
               16  LOAD_FAST                'upd_count'
               18  CALL_METHOD_1         1  ''
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          

 L. 398        24  LOAD_FAST                'upd_count'
               26  LOAD_CONST               0
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    36  'to 36'
               32  LOAD_CONST               None
               34  RETURN_VALUE     
             36_0  COME_FROM            30  '30'

 L. 400        36  LOAD_CONST               None
               38  STORE_FAST               'new_messages'

 L. 401        40  LOAD_CONST               None
               42  STORE_FAST               'new_edited_messages'

 L. 402        44  LOAD_CONST               None
               46  STORE_FAST               'new_channel_posts'

 L. 403        48  LOAD_CONST               None
               50  STORE_FAST               'new_edited_channel_posts'

 L. 404        52  LOAD_CONST               None
               54  STORE_FAST               'new_inline_queries'

 L. 405        56  LOAD_CONST               None
               58  STORE_FAST               'new_chosen_inline_results'

 L. 406        60  LOAD_CONST               None
               62  STORE_FAST               'new_callback_queries'

 L. 407        64  LOAD_CONST               None
               66  STORE_FAST               'new_shipping_queries'

 L. 408        68  LOAD_CONST               None
               70  STORE_FAST               'new_pre_checkout_queries'

 L. 409        72  LOAD_CONST               None
               74  STORE_FAST               'new_polls'

 L. 410        76  LOAD_CONST               None
               78  STORE_FAST               'new_poll_answers'

 L. 411        80  LOAD_CONST               None
               82  STORE_FAST               'new_my_chat_members'

 L. 412        84  LOAD_CONST               None
               86  STORE_FAST               'new_chat_members'

 L. 414        88  LOAD_FAST                'updates'
               90  GET_ITER         
             92_0  COME_FROM           670  '670'
             92_1  COME_FROM           642  '642'
             92_2  COME_FROM           188  '188'
            92_94  FOR_ITER            672  'to 672'
               96  STORE_FAST               'update'

 L. 415        98  LOAD_GLOBAL              apihelper
              100  LOAD_ATTR                ENABLE_MIDDLEWARE
              102  POP_JUMP_IF_FALSE   212  'to 212'

 L. 416       104  SETUP_FINALLY       120  'to 120'

 L. 417       106  LOAD_FAST                'self'
              108  LOAD_METHOD              process_middlewares
              110  LOAD_FAST                'update'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          
              116  POP_BLOCK        
              118  JUMP_FORWARD        212  'to 212'
            120_0  COME_FROM_FINALLY   104  '104'

 L. 418       120  DUP_TOP          
              122  LOAD_GLOBAL              Exception
              124  <121>               210  ''
              126  POP_TOP          
              128  STORE_FAST               'e'
              130  POP_TOP          
              132  SETUP_FINALLY       202  'to 202'

 L. 419       134  LOAD_GLOBAL              logger
              136  LOAD_METHOD              error
              138  LOAD_GLOBAL              str
              140  LOAD_FAST                'e'
              142  CALL_FUNCTION_1       1  ''
              144  CALL_METHOD_1         1  ''
              146  POP_TOP          

 L. 420       148  LOAD_FAST                'self'
              150  LOAD_ATTR                suppress_middleware_excepions
              152  POP_JUMP_IF_TRUE    158  'to 158'

 L. 421       154  RAISE_VARARGS_0       0  'reraise'
              156  JUMP_FORWARD        190  'to 190'
            158_0  COME_FROM           152  '152'

 L. 423       158  LOAD_FAST                'update'
              160  LOAD_ATTR                update_id
              162  LOAD_FAST                'self'
              164  LOAD_ATTR                last_update_id
              166  COMPARE_OP               >
              168  POP_JUMP_IF_FALSE   178  'to 178'
              170  LOAD_FAST                'update'
              172  LOAD_ATTR                update_id
              174  LOAD_FAST                'self'
              176  STORE_ATTR               last_update_id
            178_0  COME_FROM           168  '168'

 L. 424       178  POP_BLOCK        
              180  POP_EXCEPT       
              182  LOAD_CONST               None
              184  STORE_FAST               'e'
              186  DELETE_FAST              'e'
              188  JUMP_BACK            92  'to 92'
            190_0  COME_FROM           156  '156'
              190  POP_BLOCK        
              192  POP_EXCEPT       
              194  LOAD_CONST               None
              196  STORE_FAST               'e'
              198  DELETE_FAST              'e'
              200  JUMP_FORWARD        212  'to 212'
            202_0  COME_FROM_FINALLY   132  '132'
              202  LOAD_CONST               None
              204  STORE_FAST               'e'
              206  DELETE_FAST              'e'
              208  <48>             
              210  <48>             
            212_0  COME_FROM           200  '200'
            212_1  COME_FROM           118  '118'
            212_2  COME_FROM           102  '102'

 L. 426       212  LOAD_FAST                'update'
              214  LOAD_ATTR                update_id
              216  LOAD_FAST                'self'
              218  LOAD_ATTR                last_update_id
              220  COMPARE_OP               >
              222  POP_JUMP_IF_FALSE   232  'to 232'

 L. 427       224  LOAD_FAST                'update'
              226  LOAD_ATTR                update_id
              228  LOAD_FAST                'self'
              230  STORE_ATTR               last_update_id
            232_0  COME_FROM           222  '222'

 L. 428       232  LOAD_FAST                'update'
              234  LOAD_ATTR                message
          236_238  POP_JUMP_IF_FALSE   264  'to 264'

 L. 429       240  LOAD_FAST                'new_messages'
              242  LOAD_CONST               None
              244  <117>                 0  ''
              246  POP_JUMP_IF_FALSE   252  'to 252'
              248  BUILD_LIST_0          0 
              250  STORE_FAST               'new_messages'
            252_0  COME_FROM           246  '246'

 L. 430       252  LOAD_FAST                'new_messages'
              254  LOAD_METHOD              append
              256  LOAD_FAST                'update'
              258  LOAD_ATTR                message
              260  CALL_METHOD_1         1  ''
              262  POP_TOP          
            264_0  COME_FROM           236  '236'

 L. 431       264  LOAD_FAST                'update'
              266  LOAD_ATTR                edited_message
          268_270  POP_JUMP_IF_FALSE   298  'to 298'

 L. 432       272  LOAD_FAST                'new_edited_messages'
              274  LOAD_CONST               None
              276  <117>                 0  ''
          278_280  POP_JUMP_IF_FALSE   286  'to 286'
              282  BUILD_LIST_0          0 
              284  STORE_FAST               'new_edited_messages'
            286_0  COME_FROM           278  '278'

 L. 433       286  LOAD_FAST                'new_edited_messages'
              288  LOAD_METHOD              append
              290  LOAD_FAST                'update'
              292  LOAD_ATTR                edited_message
              294  CALL_METHOD_1         1  ''
              296  POP_TOP          
            298_0  COME_FROM           268  '268'

 L. 434       298  LOAD_FAST                'update'
              300  LOAD_ATTR                channel_post
          302_304  POP_JUMP_IF_FALSE   332  'to 332'

 L. 435       306  LOAD_FAST                'new_channel_posts'
              308  LOAD_CONST               None
              310  <117>                 0  ''
          312_314  POP_JUMP_IF_FALSE   320  'to 320'
              316  BUILD_LIST_0          0 
              318  STORE_FAST               'new_channel_posts'
            320_0  COME_FROM           312  '312'

 L. 436       320  LOAD_FAST                'new_channel_posts'
              322  LOAD_METHOD              append
              324  LOAD_FAST                'update'
              326  LOAD_ATTR                channel_post
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          
            332_0  COME_FROM           302  '302'

 L. 437       332  LOAD_FAST                'update'
              334  LOAD_ATTR                edited_channel_post
          336_338  POP_JUMP_IF_FALSE   366  'to 366'

 L. 438       340  LOAD_FAST                'new_edited_channel_posts'
              342  LOAD_CONST               None
              344  <117>                 0  ''
          346_348  POP_JUMP_IF_FALSE   354  'to 354'
              350  BUILD_LIST_0          0 
              352  STORE_FAST               'new_edited_channel_posts'
            354_0  COME_FROM           346  '346'

 L. 439       354  LOAD_FAST                'new_edited_channel_posts'
              356  LOAD_METHOD              append
              358  LOAD_FAST                'update'
              360  LOAD_ATTR                edited_channel_post
              362  CALL_METHOD_1         1  ''
              364  POP_TOP          
            366_0  COME_FROM           336  '336'

 L. 440       366  LOAD_FAST                'update'
              368  LOAD_ATTR                inline_query
          370_372  POP_JUMP_IF_FALSE   400  'to 400'

 L. 441       374  LOAD_FAST                'new_inline_queries'
              376  LOAD_CONST               None
              378  <117>                 0  ''
          380_382  POP_JUMP_IF_FALSE   388  'to 388'
              384  BUILD_LIST_0          0 
              386  STORE_FAST               'new_inline_queries'
            388_0  COME_FROM           380  '380'

 L. 442       388  LOAD_FAST                'new_inline_queries'
              390  LOAD_METHOD              append
              392  LOAD_FAST                'update'
              394  LOAD_ATTR                inline_query
              396  CALL_METHOD_1         1  ''
              398  POP_TOP          
            400_0  COME_FROM           370  '370'

 L. 443       400  LOAD_FAST                'update'
              402  LOAD_ATTR                chosen_inline_result
          404_406  POP_JUMP_IF_FALSE   434  'to 434'

 L. 444       408  LOAD_FAST                'new_chosen_inline_results'
              410  LOAD_CONST               None
              412  <117>                 0  ''
          414_416  POP_JUMP_IF_FALSE   422  'to 422'
              418  BUILD_LIST_0          0 
              420  STORE_FAST               'new_chosen_inline_results'
            422_0  COME_FROM           414  '414'

 L. 445       422  LOAD_FAST                'new_chosen_inline_results'
              424  LOAD_METHOD              append
              426  LOAD_FAST                'update'
              428  LOAD_ATTR                chosen_inline_result
              430  CALL_METHOD_1         1  ''
              432  POP_TOP          
            434_0  COME_FROM           404  '404'

 L. 446       434  LOAD_FAST                'update'
              436  LOAD_ATTR                callback_query
          438_440  POP_JUMP_IF_FALSE   468  'to 468'

 L. 447       442  LOAD_FAST                'new_callback_queries'
              444  LOAD_CONST               None
              446  <117>                 0  ''
          448_450  POP_JUMP_IF_FALSE   456  'to 456'
              452  BUILD_LIST_0          0 
              454  STORE_FAST               'new_callback_queries'
            456_0  COME_FROM           448  '448'

 L. 448       456  LOAD_FAST                'new_callback_queries'
              458  LOAD_METHOD              append
              460  LOAD_FAST                'update'
              462  LOAD_ATTR                callback_query
              464  CALL_METHOD_1         1  ''
              466  POP_TOP          
            468_0  COME_FROM           438  '438'

 L. 449       468  LOAD_FAST                'update'
              470  LOAD_ATTR                shipping_query
          472_474  POP_JUMP_IF_FALSE   502  'to 502'

 L. 450       476  LOAD_FAST                'new_shipping_queries'
              478  LOAD_CONST               None
              480  <117>                 0  ''
          482_484  POP_JUMP_IF_FALSE   490  'to 490'
              486  BUILD_LIST_0          0 
              488  STORE_FAST               'new_shipping_queries'
            490_0  COME_FROM           482  '482'

 L. 451       490  LOAD_FAST                'new_shipping_queries'
              492  LOAD_METHOD              append
              494  LOAD_FAST                'update'
              496  LOAD_ATTR                shipping_query
              498  CALL_METHOD_1         1  ''
              500  POP_TOP          
            502_0  COME_FROM           472  '472'

 L. 452       502  LOAD_FAST                'update'
              504  LOAD_ATTR                pre_checkout_query
          506_508  POP_JUMP_IF_FALSE   536  'to 536'

 L. 453       510  LOAD_FAST                'new_pre_checkout_queries'
              512  LOAD_CONST               None
              514  <117>                 0  ''
          516_518  POP_JUMP_IF_FALSE   524  'to 524'
              520  BUILD_LIST_0          0 
              522  STORE_FAST               'new_pre_checkout_queries'
            524_0  COME_FROM           516  '516'

 L. 454       524  LOAD_FAST                'new_pre_checkout_queries'
              526  LOAD_METHOD              append
              528  LOAD_FAST                'update'
              530  LOAD_ATTR                pre_checkout_query
              532  CALL_METHOD_1         1  ''
              534  POP_TOP          
            536_0  COME_FROM           506  '506'

 L. 455       536  LOAD_FAST                'update'
              538  LOAD_ATTR                poll
          540_542  POP_JUMP_IF_FALSE   570  'to 570'

 L. 456       544  LOAD_FAST                'new_polls'
              546  LOAD_CONST               None
              548  <117>                 0  ''
          550_552  POP_JUMP_IF_FALSE   558  'to 558'
              554  BUILD_LIST_0          0 
              556  STORE_FAST               'new_polls'
            558_0  COME_FROM           550  '550'

 L. 457       558  LOAD_FAST                'new_polls'
              560  LOAD_METHOD              append
              562  LOAD_FAST                'update'
              564  LOAD_ATTR                poll
              566  CALL_METHOD_1         1  ''
              568  POP_TOP          
            570_0  COME_FROM           540  '540'

 L. 458       570  LOAD_FAST                'update'
              572  LOAD_ATTR                poll_answer
          574_576  POP_JUMP_IF_FALSE   604  'to 604'

 L. 459       578  LOAD_FAST                'new_poll_answers'
              580  LOAD_CONST               None
              582  <117>                 0  ''
          584_586  POP_JUMP_IF_FALSE   592  'to 592'
              588  BUILD_LIST_0          0 
              590  STORE_FAST               'new_poll_answers'
            592_0  COME_FROM           584  '584'

 L. 460       592  LOAD_FAST                'new_poll_answers'
              594  LOAD_METHOD              append
              596  LOAD_FAST                'update'
              598  LOAD_ATTR                poll_answer
              600  CALL_METHOD_1         1  ''
              602  POP_TOP          
            604_0  COME_FROM           574  '574'

 L. 461       604  LOAD_FAST                'update'
              606  LOAD_ATTR                my_chat_member
          608_610  POP_JUMP_IF_FALSE   638  'to 638'

 L. 462       612  LOAD_FAST                'new_my_chat_members'
              614  LOAD_CONST               None
              616  <117>                 0  ''
          618_620  POP_JUMP_IF_FALSE   626  'to 626'
              622  BUILD_LIST_0          0 
              624  STORE_FAST               'new_my_chat_members'
            626_0  COME_FROM           618  '618'

 L. 463       626  LOAD_FAST                'new_my_chat_members'
              628  LOAD_METHOD              append
              630  LOAD_FAST                'update'
              632  LOAD_ATTR                my_chat_member
              634  CALL_METHOD_1         1  ''
              636  POP_TOP          
            638_0  COME_FROM           608  '608'

 L. 464       638  LOAD_FAST                'update'
              640  LOAD_ATTR                chat_member
              642  POP_JUMP_IF_FALSE_BACK    92  'to 92'

 L. 465       644  LOAD_FAST                'new_chat_members'
              646  LOAD_CONST               None
              648  <117>                 0  ''
          650_652  POP_JUMP_IF_FALSE   658  'to 658'
              654  BUILD_LIST_0          0 
              656  STORE_FAST               'new_chat_members'
            658_0  COME_FROM           650  '650'

 L. 466       658  LOAD_FAST                'new_chat_members'
              660  LOAD_METHOD              append
              662  LOAD_FAST                'update'
              664  LOAD_ATTR                chat_member
              666  CALL_METHOD_1         1  ''
              668  POP_TOP          
              670  JUMP_BACK            92  'to 92'
            672_0  COME_FROM            92  '92'

 L. 468       672  LOAD_FAST                'new_messages'
          674_676  POP_JUMP_IF_FALSE   688  'to 688'

 L. 469       678  LOAD_FAST                'self'
              680  LOAD_METHOD              process_new_messages
              682  LOAD_FAST                'new_messages'
              684  CALL_METHOD_1         1  ''
              686  POP_TOP          
            688_0  COME_FROM           674  '674'

 L. 470       688  LOAD_FAST                'new_edited_messages'
          690_692  POP_JUMP_IF_FALSE   704  'to 704'

 L. 471       694  LOAD_FAST                'self'
              696  LOAD_METHOD              process_new_edited_messages
              698  LOAD_FAST                'new_edited_messages'
              700  CALL_METHOD_1         1  ''
              702  POP_TOP          
            704_0  COME_FROM           690  '690'

 L. 472       704  LOAD_FAST                'new_channel_posts'
          706_708  POP_JUMP_IF_FALSE   720  'to 720'

 L. 473       710  LOAD_FAST                'self'
              712  LOAD_METHOD              process_new_channel_posts
              714  LOAD_FAST                'new_channel_posts'
              716  CALL_METHOD_1         1  ''
              718  POP_TOP          
            720_0  COME_FROM           706  '706'

 L. 474       720  LOAD_FAST                'new_edited_channel_posts'
          722_724  POP_JUMP_IF_FALSE   736  'to 736'

 L. 475       726  LOAD_FAST                'self'
              728  LOAD_METHOD              process_new_edited_channel_posts
              730  LOAD_FAST                'new_edited_channel_posts'
              732  CALL_METHOD_1         1  ''
              734  POP_TOP          
            736_0  COME_FROM           722  '722'

 L. 476       736  LOAD_FAST                'new_inline_queries'
          738_740  POP_JUMP_IF_FALSE   752  'to 752'

 L. 477       742  LOAD_FAST                'self'
              744  LOAD_METHOD              process_new_inline_query
              746  LOAD_FAST                'new_inline_queries'
              748  CALL_METHOD_1         1  ''
              750  POP_TOP          
            752_0  COME_FROM           738  '738'

 L. 478       752  LOAD_FAST                'new_chosen_inline_results'
          754_756  POP_JUMP_IF_FALSE   768  'to 768'

 L. 479       758  LOAD_FAST                'self'
              760  LOAD_METHOD              process_new_chosen_inline_query
              762  LOAD_FAST                'new_chosen_inline_results'
              764  CALL_METHOD_1         1  ''
              766  POP_TOP          
            768_0  COME_FROM           754  '754'

 L. 480       768  LOAD_FAST                'new_callback_queries'
          770_772  POP_JUMP_IF_FALSE   784  'to 784'

 L. 481       774  LOAD_FAST                'self'
              776  LOAD_METHOD              process_new_callback_query
              778  LOAD_FAST                'new_callback_queries'
              780  CALL_METHOD_1         1  ''
              782  POP_TOP          
            784_0  COME_FROM           770  '770'

 L. 482       784  LOAD_FAST                'new_shipping_queries'
          786_788  POP_JUMP_IF_FALSE   800  'to 800'

 L. 483       790  LOAD_FAST                'self'
              792  LOAD_METHOD              process_new_shipping_query
              794  LOAD_FAST                'new_shipping_queries'
              796  CALL_METHOD_1         1  ''
              798  POP_TOP          
            800_0  COME_FROM           786  '786'

 L. 484       800  LOAD_FAST                'new_pre_checkout_queries'
          802_804  POP_JUMP_IF_FALSE   816  'to 816'

 L. 485       806  LOAD_FAST                'self'
              808  LOAD_METHOD              process_new_pre_checkout_query
              810  LOAD_FAST                'new_pre_checkout_queries'
              812  CALL_METHOD_1         1  ''
              814  POP_TOP          
            816_0  COME_FROM           802  '802'

 L. 486       816  LOAD_FAST                'new_polls'
          818_820  POP_JUMP_IF_FALSE   832  'to 832'

 L. 487       822  LOAD_FAST                'self'
              824  LOAD_METHOD              process_new_poll
              826  LOAD_FAST                'new_polls'
              828  CALL_METHOD_1         1  ''
              830  POP_TOP          
            832_0  COME_FROM           818  '818'

 L. 488       832  LOAD_FAST                'new_poll_answers'
          834_836  POP_JUMP_IF_FALSE   848  'to 848'

 L. 489       838  LOAD_FAST                'self'
              840  LOAD_METHOD              process_new_poll_answer
              842  LOAD_FAST                'new_poll_answers'
              844  CALL_METHOD_1         1  ''
              846  POP_TOP          
            848_0  COME_FROM           834  '834'

 L. 490       848  LOAD_FAST                'new_my_chat_members'
          850_852  POP_JUMP_IF_FALSE   864  'to 864'

 L. 491       854  LOAD_FAST                'self'
              856  LOAD_METHOD              process_new_my_chat_member
              858  LOAD_FAST                'new_my_chat_members'
              860  CALL_METHOD_1         1  ''
              862  POP_TOP          
            864_0  COME_FROM           850  '850'

 L. 492       864  LOAD_FAST                'new_chat_members'
          866_868  POP_JUMP_IF_FALSE   880  'to 880'

 L. 493       870  LOAD_FAST                'self'
              872  LOAD_METHOD              process_new_chat_member
              874  LOAD_FAST                'new_chat_members'
              876  CALL_METHOD_1         1  ''
              878  POP_TOP          
            880_0  COME_FROM           866  '866'

Parse error at or near `<121>' instruction at offset 124

    def process_new_messages(self, new_messages):
        self._notify_next_handlers(new_messages)
        self._notify_reply_handlers(new_messages)
        self._TeleBot__notify_update(new_messages)
        self._notify_command_handlers(self.message_handlers, new_messages)

    def process_new_edited_messages(self, edited_message):
        self._notify_command_handlers(self.edited_message_handlers, edited_message)

    def process_new_channel_posts(self, channel_post):
        self._notify_command_handlers(self.channel_post_handlers, channel_post)

    def process_new_edited_channel_posts(self, edited_channel_post):
        self._notify_command_handlers(self.edited_channel_post_handlers, edited_channel_post)

    def process_new_inline_query(self, new_inline_querys):
        self._notify_command_handlers(self.inline_handlers, new_inline_querys)

    def process_new_chosen_inline_query(self, new_chosen_inline_querys):
        self._notify_command_handlers(self.chosen_inline_handlers, new_chosen_inline_querys)

    def process_new_callback_query(self, new_callback_querys):
        self._notify_command_handlers(self.callback_query_handlers, new_callback_querys)

    def process_new_shipping_query(self, new_shipping_querys):
        self._notify_command_handlers(self.shipping_query_handlers, new_shipping_querys)

    def process_new_pre_checkout_query(self, pre_checkout_querys):
        self._notify_command_handlers(self.pre_checkout_query_handlers, pre_checkout_querys)

    def process_new_poll(self, polls):
        self._notify_command_handlers(self.poll_handlers, polls)

    def process_new_poll_answer(self, poll_answers):
        self._notify_command_handlers(self.poll_answer_handlers, poll_answers)

    def process_new_my_chat_member(self, my_chat_members):
        self._notify_command_handlers(self.my_chat_member_handlers, my_chat_members)

    def process_new_chat_member(self, chat_members):
        self._notify_command_handlers(self.chat_member_handlers, chat_members)

    def process_middlewares--- This code section failed: ---

 L. 538         0  LOAD_FAST                'self'
                2  LOAD_ATTR                typed_middleware_handlers
                4  LOAD_METHOD              items
                6  CALL_METHOD_0         0  ''
                8  GET_ITER         
             10_0  COME_FROM           126  '126'
             10_1  COME_FROM            30  '30'
               10  FOR_ITER            128  'to 128'
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'update_type'
               16  STORE_FAST               'middlewares'

 L. 539        18  LOAD_GLOBAL              getattr
               20  LOAD_FAST                'update'
               22  LOAD_FAST                'update_type'
               24  CALL_FUNCTION_2       2  ''
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE_BACK    10  'to 10'

 L. 540        32  LOAD_FAST                'middlewares'
               34  GET_ITER         
             36_0  COME_FROM           124  '124'
             36_1  COME_FROM           112  '112'
             36_2  COME_FROM            60  '60'
               36  FOR_ITER            126  'to 126'
               38  STORE_FAST               'typed_middleware_handler'

 L. 541        40  SETUP_FINALLY        62  'to 62'

 L. 542        42  LOAD_FAST                'typed_middleware_handler'
               44  LOAD_FAST                'self'
               46  LOAD_GLOBAL              getattr
               48  LOAD_FAST                'update'
               50  LOAD_FAST                'update_type'
               52  CALL_FUNCTION_2       2  ''
               54  CALL_FUNCTION_2       2  ''
               56  POP_TOP          
               58  POP_BLOCK        
               60  JUMP_BACK            36  'to 36'
             62_0  COME_FROM_FINALLY    40  '40'

 L. 543        62  DUP_TOP          
               64  LOAD_GLOBAL              Exception
               66  <121>               122  ''
               68  POP_TOP          
               70  STORE_FAST               'e'
               72  POP_TOP          
               74  SETUP_FINALLY       114  'to 114'

 L. 544        76  LOAD_FAST                'e'
               78  LOAD_ATTR                args
               80  LOAD_STR                 'Typed middleware handler "'
               82  LOAD_FAST                'typed_middleware_handler'
               84  LOAD_ATTR                __qualname__
               86  FORMAT_VALUE          0  ''
               88  LOAD_STR                 '"'
               90  BUILD_STRING_3        3 
               92  BUILD_TUPLE_1         1 
               94  BINARY_ADD       
               96  LOAD_FAST                'e'
               98  STORE_ATTR               args

 L. 545       100  RAISE_VARARGS_0       0  'reraise'
              102  POP_BLOCK        
              104  POP_EXCEPT       
              106  LOAD_CONST               None
              108  STORE_FAST               'e'
              110  DELETE_FAST              'e'
              112  JUMP_BACK            36  'to 36'
            114_0  COME_FROM_FINALLY    74  '74'
              114  LOAD_CONST               None
              116  STORE_FAST               'e'
              118  DELETE_FAST              'e'
              120  <48>             
              122  <48>             
              124  JUMP_BACK            36  'to 36'
            126_0  COME_FROM            36  '36'
              126  JUMP_BACK            10  'to 10'
            128_0  COME_FROM            10  '10'

 L. 547       128  LOAD_GLOBAL              len
              130  LOAD_FAST                'self'
              132  LOAD_ATTR                default_middleware_handlers
              134  CALL_FUNCTION_1       1  ''
              136  LOAD_CONST               0
              138  COMPARE_OP               >
              140  POP_JUMP_IF_FALSE   232  'to 232'

 L. 548       142  LOAD_FAST                'self'
              144  LOAD_ATTR                default_middleware_handlers
              146  GET_ITER         
            148_0  COME_FROM           230  '230'
            148_1  COME_FROM           218  '218'
            148_2  COME_FROM           166  '166'
              148  FOR_ITER            232  'to 232'
              150  STORE_FAST               'default_middleware_handler'

 L. 549       152  SETUP_FINALLY       168  'to 168'

 L. 550       154  LOAD_FAST                'default_middleware_handler'
              156  LOAD_FAST                'self'
              158  LOAD_FAST                'update'
              160  CALL_FUNCTION_2       2  ''
              162  POP_TOP          
              164  POP_BLOCK        
              166  JUMP_BACK           148  'to 148'
            168_0  COME_FROM_FINALLY   152  '152'

 L. 551       168  DUP_TOP          
              170  LOAD_GLOBAL              Exception
              172  <121>               228  ''
              174  POP_TOP          
              176  STORE_FAST               'e'
              178  POP_TOP          
              180  SETUP_FINALLY       220  'to 220'

 L. 552       182  LOAD_FAST                'e'
              184  LOAD_ATTR                args
              186  LOAD_STR                 'Default middleware handler "'
              188  LOAD_FAST                'default_middleware_handler'
              190  LOAD_ATTR                __qualname__
              192  FORMAT_VALUE          0  ''
              194  LOAD_STR                 '"'
              196  BUILD_STRING_3        3 
              198  BUILD_TUPLE_1         1 
              200  BINARY_ADD       
              202  LOAD_FAST                'e'
              204  STORE_ATTR               args

 L. 553       206  RAISE_VARARGS_0       0  'reraise'
              208  POP_BLOCK        
              210  POP_EXCEPT       
              212  LOAD_CONST               None
              214  STORE_FAST               'e'
              216  DELETE_FAST              'e'
              218  JUMP_BACK           148  'to 148'
            220_0  COME_FROM_FINALLY   180  '180'
              220  LOAD_CONST               None
              222  STORE_FAST               'e'
              224  DELETE_FAST              'e'
              226  <48>             
              228  <48>             
              230  JUMP_BACK           148  'to 148'
            232_0  COME_FROM           148  '148'
            232_1  COME_FROM           140  '140'

Parse error at or near `<117>' instruction at offset 28

    def __notify_update(self, new_messages):
        if len(self.update_listener) == 0:
            return
        for listener in self.update_listener:
            self._exec_task(listener, new_messages)

    def infinity_polling--- This code section failed: ---
              0_0  COME_FROM           184  '184'
              0_1  COME_FROM           172  '172'
              0_2  COME_FROM           162  '162'
              0_3  COME_FROM           136  '136'

 L. 579         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _TeleBot__stop_polling
                4  LOAD_METHOD              is_set
                6  CALL_METHOD_0         0  ''
                8  POP_JUMP_IF_TRUE    186  'to 186'

 L. 580        10  SETUP_FINALLY        42  'to 42'

 L. 581        12  LOAD_FAST                'self'
               14  LOAD_ATTR                polling

 L. 582        16  LOAD_FAST                'args'

 L. 581        18  LOAD_CONST               True
               20  LOAD_FAST                'timeout'
               22  LOAD_FAST                'long_polling_timeout'

 L. 582        24  LOAD_FAST                'allowed_updates'

 L. 581        26  LOAD_CONST               ('none_stop', 'timeout', 'long_polling_timeout', 'allowed_updates')
               28  BUILD_CONST_KEY_MAP_4     4 

 L. 582        30  LOAD_FAST                'kwargs'

 L. 581        32  <164>                 1  ''
               34  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               36  POP_TOP          
               38  POP_BLOCK        
               40  JUMP_FORWARD        160  'to 160'
             42_0  COME_FROM_FINALLY    10  '10'

 L. 583        42  DUP_TOP          
               44  LOAD_GLOBAL              Exception
               46  <121>               158  ''
               48  POP_TOP          
               50  STORE_FAST               'e'
               52  POP_TOP          
               54  SETUP_FINALLY       150  'to 150'

 L. 584        56  LOAD_FAST                'logger_level'
               58  POP_JUMP_IF_FALSE    86  'to 86'
               60  LOAD_FAST                'logger_level'
               62  LOAD_GLOBAL              logging
               64  LOAD_ATTR                ERROR
               66  COMPARE_OP               >=
               68  POP_JUMP_IF_FALSE    86  'to 86'

 L. 585        70  LOAD_GLOBAL              logger
               72  LOAD_METHOD              error
               74  LOAD_STR                 'Infinity polling exception: %s'
               76  LOAD_GLOBAL              str
               78  LOAD_FAST                'e'
               80  CALL_FUNCTION_1       1  ''
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          
             86_0  COME_FROM            68  '68'
             86_1  COME_FROM            58  '58'

 L. 586        86  LOAD_FAST                'logger_level'
               88  POP_JUMP_IF_FALSE   116  'to 116'
               90  LOAD_FAST                'logger_level'
               92  LOAD_GLOBAL              logging
               94  LOAD_ATTR                DEBUG
               96  COMPARE_OP               >=
               98  POP_JUMP_IF_FALSE   116  'to 116'

 L. 587       100  LOAD_GLOBAL              logger
              102  LOAD_METHOD              error
              104  LOAD_STR                 'Exception traceback:\n%s'
              106  LOAD_GLOBAL              traceback
              108  LOAD_METHOD              format_exc
              110  CALL_METHOD_0         0  ''
              112  CALL_METHOD_2         2  ''
              114  POP_TOP          
            116_0  COME_FROM            98  '98'
            116_1  COME_FROM            88  '88'

 L. 588       116  LOAD_GLOBAL              time
              118  LOAD_METHOD              sleep
              120  LOAD_CONST               3
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L. 589       126  POP_BLOCK        
              128  POP_EXCEPT       
              130  LOAD_CONST               None
              132  STORE_FAST               'e'
              134  DELETE_FAST              'e'
              136  JUMP_BACK             0  'to 0'
              138  POP_BLOCK        
              140  POP_EXCEPT       
              142  LOAD_CONST               None
              144  STORE_FAST               'e'
              146  DELETE_FAST              'e'
              148  JUMP_FORWARD        160  'to 160'
            150_0  COME_FROM_FINALLY    54  '54'
              150  LOAD_CONST               None
              152  STORE_FAST               'e'
              154  DELETE_FAST              'e'
              156  <48>             
              158  <48>             
            160_0  COME_FROM           148  '148'
            160_1  COME_FROM            40  '40'

 L. 590       160  LOAD_FAST                'logger_level'
              162  POP_JUMP_IF_FALSE_BACK     0  'to 0'
              164  LOAD_FAST                'logger_level'
              166  LOAD_GLOBAL              logging
              168  LOAD_ATTR                INFO
              170  COMPARE_OP               >=
              172  POP_JUMP_IF_FALSE_BACK     0  'to 0'

 L. 591       174  LOAD_GLOBAL              logger
              176  LOAD_METHOD              error
              178  LOAD_STR                 'Infinity polling: polling exited'
              180  CALL_METHOD_1         1  ''
              182  POP_TOP          
              184  JUMP_BACK             0  'to 0'
            186_0  COME_FROM             8  '8'

 L. 592       186  LOAD_FAST                'logger_level'
              188  POP_JUMP_IF_FALSE   210  'to 210'
              190  LOAD_FAST                'logger_level'
              192  LOAD_GLOBAL              logging
              194  LOAD_ATTR                INFO
              196  COMPARE_OP               >=
              198  POP_JUMP_IF_FALSE   210  'to 210'

 L. 593       200  LOAD_GLOBAL              logger
              202  LOAD_METHOD              error
              204  LOAD_STR                 'Break infinity polling'
              206  CALL_METHOD_1         1  ''
              208  POP_TOP          
            210_0  COME_FROM           198  '198'
            210_1  COME_FROM           188  '188'

Parse error at or near `<164>' instruction at offset 32

    def polling(self, none_stop: bool=False, interval: int=0, timeout: int=20, long_polling_timeout: int=20, allowed_updates: Optional[List[str]]=None):
        """
        This function creates a new Thread that calls an internal __retrieve_updates function.
        This allows the bot to retrieve Updates automagically and notify listeners and message handlers accordingly.

        Warning: Do not call this function more than once!

        Always get updates.
        :param interval: Delay between two update retrivals
        :param none_stop: Do not stop polling when an ApiException occurs.
        :param timeout: Request connection timeout
        :param long_polling_timeout: Timeout in seconds for long polling (see API docs)
        :param allowed_updates: A list of the update types you want your bot to receive.
            For example, specify [“message”, “edited_channel_post”, “callback_query”] to only receive updates of these types. 
            See util.update_types for a complete list of available update types. 
            Specify an empty list to receive all update types except chat_member (default). 
            If not specified, the previous setting will be used.
            
            Please note that this parameter doesn't affect updates created before the call to the get_updates, 
            so unwanted updates may be received for a short period of time.
        :return:
        """
        if self.threaded:
            self._TeleBot__threaded_polling(none_stop, interval, timeout, long_polling_timeout, allowed_updates)
        else:
            self._TeleBot__non_threaded_polling(none_stop, interval, timeout, long_polling_timeout, allowed_updates)

    def __threaded_polling--- This code section failed: ---

 L. 624         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              info
                4  LOAD_STR                 'Started polling.'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 625        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _TeleBot__stop_polling
               14  LOAD_METHOD              clear
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 626        20  LOAD_CONST               0.25
               22  STORE_FAST               'error_interval'

 L. 628        24  LOAD_GLOBAL              util
               26  LOAD_ATTR                WorkerThread
               28  LOAD_STR                 'PollingThread'
               30  LOAD_CONST               ('name',)
               32  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               34  STORE_FAST               'polling_thread'

 L. 629        36  LOAD_GLOBAL              util
               38  LOAD_METHOD              OrEvent

 L. 630        40  LOAD_FAST                'polling_thread'
               42  LOAD_ATTR                done_event

 L. 631        44  LOAD_FAST                'polling_thread'
               46  LOAD_ATTR                exception_event

 L. 632        48  LOAD_FAST                'self'
               50  LOAD_ATTR                worker_pool
               52  LOAD_ATTR                exception_event

 L. 629        54  CALL_METHOD_3         3  ''
               56  STORE_FAST               'or_event'
             58_0  COME_FROM           486  '486'
             58_1  COME_FROM           474  '474'
             58_2  COME_FROM           350  '350'
             58_3  COME_FROM           298  '298'
             58_4  COME_FROM           134  '134'

 L. 635        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _TeleBot__stop_polling
               62  LOAD_METHOD              wait
               64  LOAD_FAST                'interval'
               66  CALL_METHOD_1         1  ''
            68_70  POP_JUMP_IF_TRUE    488  'to 488'

 L. 636        72  LOAD_FAST                'or_event'
               74  LOAD_METHOD              clear
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          

 L. 637        80  SETUP_FINALLY       136  'to 136'

 L. 638        82  LOAD_FAST                'polling_thread'
               84  LOAD_ATTR                put
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                _TeleBot__retrieve_updates
               90  LOAD_FAST                'timeout'
               92  LOAD_FAST                'long_polling_timeout'
               94  LOAD_FAST                'allowed_updates'
               96  LOAD_CONST               ('allowed_updates',)
               98  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              100  POP_TOP          

 L. 639       102  LOAD_FAST                'or_event'
              104  LOAD_METHOD              wait
              106  CALL_METHOD_0         0  ''
              108  POP_TOP          

 L. 640       110  LOAD_FAST                'polling_thread'
              112  LOAD_METHOD              raise_exceptions
              114  CALL_METHOD_0         0  ''
              116  POP_TOP          

 L. 641       118  LOAD_FAST                'self'
              120  LOAD_ATTR                worker_pool
              122  LOAD_METHOD              raise_exceptions
              124  CALL_METHOD_0         0  ''
              126  POP_TOP          

 L. 642       128  LOAD_CONST               0.25
              130  STORE_FAST               'error_interval'
              132  POP_BLOCK        
              134  JUMP_BACK            58  'to 58'
            136_0  COME_FROM_FINALLY    80  '80'

 L. 643       136  DUP_TOP          
              138  LOAD_GLOBAL              apihelper
              140  LOAD_ATTR                ApiException
          142_144  <121>               308  ''
              146  POP_TOP          
              148  STORE_FAST               'e'
              150  POP_TOP          
              152  SETUP_FINALLY       300  'to 300'

 L. 644       154  LOAD_FAST                'self'
              156  LOAD_ATTR                exception_handler
              158  LOAD_CONST               None
              160  <117>                 1  ''
              162  POP_JUMP_IF_FALSE   178  'to 178'

 L. 645       164  LOAD_FAST                'self'
              166  LOAD_ATTR                exception_handler
              168  LOAD_METHOD              handle
              170  LOAD_FAST                'e'
              172  CALL_METHOD_1         1  ''
              174  STORE_FAST               'handled'
              176  JUMP_FORWARD        182  'to 182'
            178_0  COME_FROM           162  '162'

 L. 647       178  LOAD_CONST               False
              180  STORE_FAST               'handled'
            182_0  COME_FROM           176  '176'

 L. 648       182  LOAD_FAST                'handled'
          184_186  POP_JUMP_IF_TRUE    260  'to 260'

 L. 649       188  LOAD_GLOBAL              logger
              190  LOAD_METHOD              error
              192  LOAD_FAST                'e'
              194  CALL_METHOD_1         1  ''
              196  POP_TOP          

 L. 650       198  LOAD_FAST                'non_stop'
              200  POP_JUMP_IF_TRUE    224  'to 224'

 L. 651       202  LOAD_FAST                'self'
              204  LOAD_ATTR                _TeleBot__stop_polling
              206  LOAD_METHOD              set
              208  CALL_METHOD_0         0  ''
              210  POP_TOP          

 L. 652       212  LOAD_GLOBAL              logger
              214  LOAD_METHOD              info
              216  LOAD_STR                 'Exception occurred. Stopping.'
              218  CALL_METHOD_1         1  ''
              220  POP_TOP          
              222  JUMP_FORWARD        258  'to 258'
            224_0  COME_FROM           200  '200'

 L. 656       224  LOAD_GLOBAL              logger
              226  LOAD_METHOD              info
              228  LOAD_STR                 'Waiting for {0} seconds until retry'
              230  LOAD_METHOD              format
              232  LOAD_FAST                'error_interval'
              234  CALL_METHOD_1         1  ''
              236  CALL_METHOD_1         1  ''
              238  POP_TOP          

 L. 657       240  LOAD_GLOBAL              time
              242  LOAD_METHOD              sleep
              244  LOAD_FAST                'error_interval'
              246  CALL_METHOD_1         1  ''
              248  POP_TOP          

 L. 658       250  LOAD_FAST                'error_interval'
              252  LOAD_CONST               2
              254  INPLACE_MULTIPLY 
              256  STORE_FAST               'error_interval'
            258_0  COME_FROM           222  '222'
              258  JUMP_FORWARD        270  'to 270'
            260_0  COME_FROM           184  '184'

 L. 662       260  LOAD_GLOBAL              time
              262  LOAD_METHOD              sleep
              264  LOAD_FAST                'error_interval'
              266  CALL_METHOD_1         1  ''
              268  POP_TOP          
            270_0  COME_FROM           258  '258'

 L. 663       270  LOAD_FAST                'polling_thread'
              272  LOAD_METHOD              clear_exceptions
              274  CALL_METHOD_0         0  ''
              276  POP_TOP          

 L. 664       278  LOAD_FAST                'self'
              280  LOAD_ATTR                worker_pool
              282  LOAD_METHOD              clear_exceptions
              284  CALL_METHOD_0         0  ''
              286  POP_TOP          
              288  POP_BLOCK        
              290  POP_EXCEPT       
              292  LOAD_CONST               None
              294  STORE_FAST               'e'
              296  DELETE_FAST              'e'
              298  JUMP_BACK            58  'to 58'
            300_0  COME_FROM_FINALLY   152  '152'
              300  LOAD_CONST               None
              302  STORE_FAST               'e'
              304  DELETE_FAST              'e'
              306  <48>             

 L. 665       308  DUP_TOP          
              310  LOAD_GLOBAL              KeyboardInterrupt
          312_314  <121>               352  ''
              316  POP_TOP          
              318  POP_TOP          
              320  POP_TOP          

 L. 666       322  LOAD_GLOBAL              logger
              324  LOAD_METHOD              info
              326  LOAD_STR                 'KeyboardInterrupt received.'
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          

 L. 667       332  LOAD_FAST                'self'
              334  LOAD_ATTR                _TeleBot__stop_polling
              336  LOAD_METHOD              set
              338  CALL_METHOD_0         0  ''
              340  POP_TOP          

 L. 668       342  POP_EXCEPT       
          344_346  BREAK_LOOP          488  'to 488'
              348  POP_EXCEPT       
              350  JUMP_BACK            58  'to 58'

 L. 669       352  DUP_TOP          
              354  LOAD_GLOBAL              Exception
          356_358  <121>               484  ''
              360  POP_TOP          
              362  STORE_FAST               'e'
              364  POP_TOP          
              366  SETUP_FINALLY       476  'to 476'

 L. 670       368  LOAD_FAST                'self'
              370  LOAD_ATTR                exception_handler
              372  LOAD_CONST               None
              374  <117>                 1  ''
          376_378  POP_JUMP_IF_FALSE   394  'to 394'

 L. 671       380  LOAD_FAST                'self'
              382  LOAD_ATTR                exception_handler
              384  LOAD_METHOD              handle
              386  LOAD_FAST                'e'
              388  CALL_METHOD_1         1  ''
              390  STORE_FAST               'handled'
              392  JUMP_FORWARD        398  'to 398'
            394_0  COME_FROM           376  '376'

 L. 673       394  LOAD_CONST               False
              396  STORE_FAST               'handled'
            398_0  COME_FROM           392  '392'

 L. 674       398  LOAD_FAST                'handled'
          400_402  POP_JUMP_IF_TRUE    436  'to 436'

 L. 675       404  LOAD_FAST                'polling_thread'
              406  LOAD_METHOD              stop
              408  CALL_METHOD_0         0  ''
              410  POP_TOP          

 L. 676       412  LOAD_FAST                'polling_thread'
              414  LOAD_METHOD              clear_exceptions
              416  CALL_METHOD_0         0  ''
              418  POP_TOP          

 L. 677       420  LOAD_FAST                'self'
              422  LOAD_ATTR                worker_pool
              424  LOAD_METHOD              clear_exceptions
              426  CALL_METHOD_0         0  ''
              428  POP_TOP          

 L. 678       430  LOAD_FAST                'e'
              432  RAISE_VARARGS_1       1  'exception instance'
              434  JUMP_FORWARD        464  'to 464'
            436_0  COME_FROM           400  '400'

 L. 680       436  LOAD_FAST                'polling_thread'
              438  LOAD_METHOD              clear_exceptions
              440  CALL_METHOD_0         0  ''
              442  POP_TOP          

 L. 681       444  LOAD_FAST                'self'
              446  LOAD_ATTR                worker_pool
              448  LOAD_METHOD              clear_exceptions
              450  CALL_METHOD_0         0  ''
              452  POP_TOP          

 L. 682       454  LOAD_GLOBAL              time
              456  LOAD_METHOD              sleep
              458  LOAD_FAST                'error_interval'
              460  CALL_METHOD_1         1  ''
              462  POP_TOP          
            464_0  COME_FROM           434  '434'
              464  POP_BLOCK        
              466  POP_EXCEPT       
              468  LOAD_CONST               None
              470  STORE_FAST               'e'
              472  DELETE_FAST              'e'
              474  JUMP_BACK            58  'to 58'
            476_0  COME_FROM_FINALLY   366  '366'
              476  LOAD_CONST               None
              478  STORE_FAST               'e'
              480  DELETE_FAST              'e'
              482  <48>             
              484  <48>             
              486  JUMP_BACK            58  'to 58'
            488_0  COME_FROM           344  '344'
            488_1  COME_FROM            68  '68'

 L. 684       488  LOAD_FAST                'polling_thread'
              490  LOAD_METHOD              stop
              492  CALL_METHOD_0         0  ''
              494  POP_TOP          

 L. 685       496  LOAD_FAST                'polling_thread'
              498  LOAD_METHOD              clear_exceptions
              500  CALL_METHOD_0         0  ''
              502  POP_TOP          

 L. 686       504  LOAD_FAST                'self'
              506  LOAD_ATTR                worker_pool
              508  LOAD_METHOD              clear_exceptions
              510  CALL_METHOD_0         0  ''
              512  POP_TOP          

 L. 687       514  LOAD_GLOBAL              logger
              516  LOAD_METHOD              info
              518  LOAD_STR                 'Stopped polling.'
              520  CALL_METHOD_1         1  ''
              522  POP_TOP          

Parse error at or near `<121>' instruction at offset 142_144

    def __non_threaded_polling--- This code section failed: ---

 L. 690         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              info
                4  LOAD_STR                 'Started polling.'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 691        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _TeleBot__stop_polling
               14  LOAD_METHOD              clear
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 692        20  LOAD_CONST               0.25
               22  STORE_FAST               'error_interval'
             24_0  COME_FROM           348  '348'
             24_1  COME_FROM           336  '336'
             24_2  COME_FROM           256  '256'
             24_3  COME_FROM           204  '204'
             24_4  COME_FROM            62  '62'

 L. 694        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _TeleBot__stop_polling
               28  LOAD_METHOD              wait
               30  LOAD_FAST                'interval'
               32  CALL_METHOD_1         1  ''
            34_36  POP_JUMP_IF_TRUE    350  'to 350'

 L. 695        38  SETUP_FINALLY        64  'to 64'

 L. 696        40  LOAD_FAST                'self'
               42  LOAD_ATTR                _TeleBot__retrieve_updates
               44  LOAD_FAST                'timeout'
               46  LOAD_FAST                'long_polling_timeout'
               48  LOAD_FAST                'allowed_updates'
               50  LOAD_CONST               ('allowed_updates',)
               52  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               54  POP_TOP          

 L. 697        56  LOAD_CONST               0.25
               58  STORE_FAST               'error_interval'
               60  POP_BLOCK        
               62  JUMP_BACK            24  'to 24'
             64_0  COME_FROM_FINALLY    38  '38'

 L. 698        64  DUP_TOP          
               66  LOAD_GLOBAL              apihelper
               68  LOAD_ATTR                ApiException
               70  <121>               214  ''
               72  POP_TOP          
               74  STORE_FAST               'e'
               76  POP_TOP          
               78  SETUP_FINALLY       206  'to 206'

 L. 699        80  LOAD_FAST                'self'
               82  LOAD_ATTR                exception_handler
               84  LOAD_CONST               None
               86  <117>                 1  ''
               88  POP_JUMP_IF_FALSE   104  'to 104'

 L. 700        90  LOAD_FAST                'self'
               92  LOAD_ATTR                exception_handler
               94  LOAD_METHOD              handle
               96  LOAD_FAST                'e'
               98  CALL_METHOD_1         1  ''
              100  STORE_FAST               'handled'
              102  JUMP_FORWARD        108  'to 108'
            104_0  COME_FROM            88  '88'

 L. 702       104  LOAD_CONST               False
              106  STORE_FAST               'handled'
            108_0  COME_FROM           102  '102'

 L. 704       108  LOAD_FAST                'handled'
              110  POP_JUMP_IF_TRUE    184  'to 184'

 L. 705       112  LOAD_GLOBAL              logger
              114  LOAD_METHOD              error
              116  LOAD_FAST                'e'
              118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L. 706       122  LOAD_FAST                'non_stop'
              124  POP_JUMP_IF_TRUE    148  'to 148'

 L. 707       126  LOAD_FAST                'self'
              128  LOAD_ATTR                _TeleBot__stop_polling
              130  LOAD_METHOD              set
              132  CALL_METHOD_0         0  ''
              134  POP_TOP          

 L. 708       136  LOAD_GLOBAL              logger
              138  LOAD_METHOD              info
              140  LOAD_STR                 'Exception occurred. Stopping.'
              142  CALL_METHOD_1         1  ''
              144  POP_TOP          
              146  JUMP_FORWARD        194  'to 194'
            148_0  COME_FROM           124  '124'

 L. 710       148  LOAD_GLOBAL              logger
              150  LOAD_METHOD              info
              152  LOAD_STR                 'Waiting for {0} seconds until retry'
              154  LOAD_METHOD              format
              156  LOAD_FAST                'error_interval'
              158  CALL_METHOD_1         1  ''
              160  CALL_METHOD_1         1  ''
              162  POP_TOP          

 L. 711       164  LOAD_GLOBAL              time
              166  LOAD_METHOD              sleep
              168  LOAD_FAST                'error_interval'
              170  CALL_METHOD_1         1  ''
              172  POP_TOP          

 L. 712       174  LOAD_FAST                'error_interval'
              176  LOAD_CONST               2
              178  INPLACE_MULTIPLY 
              180  STORE_FAST               'error_interval'
              182  JUMP_FORWARD        194  'to 194'
            184_0  COME_FROM           110  '110'

 L. 714       184  LOAD_GLOBAL              time
              186  LOAD_METHOD              sleep
              188  LOAD_FAST                'error_interval'
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          
            194_0  COME_FROM           182  '182'
            194_1  COME_FROM           146  '146'
              194  POP_BLOCK        
              196  POP_EXCEPT       
              198  LOAD_CONST               None
              200  STORE_FAST               'e'
              202  DELETE_FAST              'e'
              204  JUMP_BACK            24  'to 24'
            206_0  COME_FROM_FINALLY    78  '78'
              206  LOAD_CONST               None
              208  STORE_FAST               'e'
              210  DELETE_FAST              'e'
              212  <48>             

 L. 715       214  DUP_TOP          
              216  LOAD_GLOBAL              KeyboardInterrupt
          218_220  <121>               258  ''
              222  POP_TOP          
              224  POP_TOP          
              226  POP_TOP          

 L. 716       228  LOAD_GLOBAL              logger
              230  LOAD_METHOD              info
              232  LOAD_STR                 'KeyboardInterrupt received.'
              234  CALL_METHOD_1         1  ''
              236  POP_TOP          

 L. 717       238  LOAD_FAST                'self'
              240  LOAD_ATTR                _TeleBot__stop_polling
              242  LOAD_METHOD              set
              244  CALL_METHOD_0         0  ''
              246  POP_TOP          

 L. 718       248  POP_EXCEPT       
          250_252  BREAK_LOOP          350  'to 350'
              254  POP_EXCEPT       
              256  JUMP_BACK            24  'to 24'

 L. 719       258  DUP_TOP          
              260  LOAD_GLOBAL              Exception
          262_264  <121>               346  ''
              266  POP_TOP          
              268  STORE_FAST               'e'
              270  POP_TOP          
              272  SETUP_FINALLY       338  'to 338'

 L. 720       274  LOAD_FAST                'self'
              276  LOAD_ATTR                exception_handler
              278  LOAD_CONST               None
              280  <117>                 1  ''
          282_284  POP_JUMP_IF_FALSE   300  'to 300'

 L. 721       286  LOAD_FAST                'self'
              288  LOAD_ATTR                exception_handler
              290  LOAD_METHOD              handle
              292  LOAD_FAST                'e'
              294  CALL_METHOD_1         1  ''
              296  STORE_FAST               'handled'
              298  JUMP_FORWARD        304  'to 304'
            300_0  COME_FROM           282  '282'

 L. 723       300  LOAD_CONST               False
              302  STORE_FAST               'handled'
            304_0  COME_FROM           298  '298'

 L. 724       304  LOAD_FAST                'handled'
          306_308  POP_JUMP_IF_TRUE    316  'to 316'

 L. 725       310  LOAD_FAST                'e'
              312  RAISE_VARARGS_1       1  'exception instance'
              314  JUMP_FORWARD        326  'to 326'
            316_0  COME_FROM           306  '306'

 L. 727       316  LOAD_GLOBAL              time
              318  LOAD_METHOD              sleep
              320  LOAD_FAST                'error_interval'
              322  CALL_METHOD_1         1  ''
              324  POP_TOP          
            326_0  COME_FROM           314  '314'
              326  POP_BLOCK        
              328  POP_EXCEPT       
              330  LOAD_CONST               None
              332  STORE_FAST               'e'
              334  DELETE_FAST              'e'
              336  JUMP_BACK            24  'to 24'
            338_0  COME_FROM_FINALLY   272  '272'
              338  LOAD_CONST               None
              340  STORE_FAST               'e'
              342  DELETE_FAST              'e'
              344  <48>             
              346  <48>             
              348  JUMP_BACK            24  'to 24'
            350_0  COME_FROM           250  '250'
            350_1  COME_FROM            34  '34'

 L. 729       350  LOAD_GLOBAL              logger
              352  LOAD_METHOD              info
              354  LOAD_STR                 'Stopped polling.'
              356  CALL_METHOD_1         1  ''
              358  POP_TOP          

Parse error at or near `<121>' instruction at offset 70

    def _exec_task--- This code section failed: ---

 L. 732         0  LOAD_FAST                'self'
                2  LOAD_ATTR                threaded
                4  POP_JUMP_IF_FALSE    34  'to 34'

 L. 733         6  LOAD_FAST                'self'
                8  LOAD_ATTR                worker_pool
               10  LOAD_ATTR                put
               12  LOAD_FAST                'task'
               14  BUILD_LIST_1          1 
               16  LOAD_FAST                'args'
               18  CALL_FINALLY         21  'to 21'
               20  WITH_CLEANUP_FINISH
               22  BUILD_MAP_0           0 
               24  LOAD_FAST                'kwargs'
               26  <164>                 1  ''
               28  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               30  POP_TOP          
               32  JUMP_FORWARD         48  'to 48'
             34_0  COME_FROM             4  '4'

 L. 735        34  LOAD_FAST                'task'
               36  LOAD_FAST                'args'
               38  BUILD_MAP_0           0 
               40  LOAD_FAST                'kwargs'
               42  <164>                 1  ''
               44  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               46  POP_TOP          
             48_0  COME_FROM            32  '32'

Parse error at or near `CALL_FINALLY' instruction at offset 18

    def stop_polling(self):
        self._TeleBot__stop_polling.set()

    def stop_bot(self):
        self.stop_polling()
        if self.worker_pool:
            self.worker_pool.close()

    def set_update_listener(self, listener):
        self.update_listener.append(listener)

    def get_me(self) -> types.User:
        """
        Returns basic information about the bot in form of a User object.
        """
        result = apihelper.get_me(self.token)
        return types.User.de_json(result)

    def get_file(self, file_id: str) -> types.File:
        """
        Use this method to get basic info about a file and prepare it for downloading.
        For the moment, bots can download files of up to 20MB in size. 
        On success, a File object is returned. 
        It is guaranteed that the link will be valid for at least 1 hour. 
        When the link expires, a new one can be requested by calling get_file again.
        """
        return types.File.de_json(apihelper.get_file(self.token, file_id))

    def get_file_url(self, file_id: str) -> str:
        return apihelper.get_file_url(self.token, file_id)

    def download_file(self, file_path: str) -> bytes:
        return apihelper.download_file(self.token, file_path)

    def log_out(self) -> bool:
        """
        Use this method to log out from the cloud Bot API server before launching the bot locally. 
        You MUST log out the bot before running it locally, otherwise there is no guarantee
        that the bot will receive updates.
        After a successful call, you can immediately log in on a local server, 
        but will not be able to log in back to the cloud Bot API server for 10 minutes. 
        Returns True on success.
        """
        return apihelper.log_out(self.token)

    def close(self) -> bool:
        """
        Use this method to close the bot instance before moving it from one local server to another. 
        You need to delete the webhook before calling this method to ensure that the bot isn't launched again
        after server restart.
        The method will return error 429 in the first 10 minutes after the bot is launched. 
        Returns True on success.
        """
        return apihelper.close(self.token)

    def get_user_profile_photos(self, user_id: int, offset: Optional[int]=None, limit: Optional[int]=None) -> types.UserProfilePhotos:
        """
        Retrieves the user profile photos of the person with 'user_id'
        See https://core.telegram.org/bots/api#getuserprofilephotos
        :param user_id:
        :param offset:
        :param limit:
        :return: API reply.
        """
        result = apihelper.get_user_profile_photos(self.token, user_id, offset, limit)
        return types.UserProfilePhotos.de_json(result)

    def get_chat(self, chat_id: Union[(int, str)]) -> types.Chat:
        """
        Use this method to get up to date information about the chat (current name of the user for one-on-one
        conversations, current username of a user, group or channel, etc.). Returns a Chat object on success.
        :param chat_id:
        :return:
        """
        result = apihelper.get_chat(self.token, chat_id)
        return types.Chat.de_json(result)

    def leave_chat(self, chat_id: Union[(int, str)]) -> bool:
        """
        Use this method for your bot to leave a group, supergroup or channel. Returns True on success.
        :param chat_id:
        :return:
        """
        result = apihelper.leave_chat(self.token, chat_id)
        return result

    def get_chat_administrators(self, chat_id: Union[(int, str)]) -> List[types.ChatMember]:
        """
        Use this method to get a list of administrators in a chat.
        On success, returns an Array of ChatMember objects that contains
            information about all chat administrators except other bots.
        :param chat_id: Unique identifier for the target chat or username
            of the target supergroup or channel (in the format @channelusername)
        :return:
        """
        result = apihelper.get_chat_administrators(self.token, chat_id)
        ret = []
        for r in result:
            ret.append(types.ChatMember.de_json(r))
        else:
            return ret

    def get_chat_members_count(self, chat_id: Union[(int, str)]) -> int:
        """
        Use this method to get the number of members in a chat. Returns Int on success.
        :param chat_id:
        :return:
        """
        result = apihelper.get_chat_members_count(self.token, chat_id)
        return result

    def set_chat_sticker_set(self, chat_id: Union[(int, str)], sticker_set_name: str) -> types.StickerSet:
        """
        Use this method to set a new group sticker set for a supergroup. The bot must be an administrator
        in the chat for this to work and must have the appropriate admin rights.
        Use the field can_set_sticker_set optionally returned in getChat requests to check
        if the bot can use this method. Returns True on success.
        :param chat_id: Unique identifier for the target chat or username of the target supergroup
        (in the format @supergroupusername)
        :param sticker_set_name: Name of the sticker set to be set as the group sticker set
        :return:
        """
        result = apihelper.set_chat_sticker_set(self.token, chat_id, sticker_set_name)
        return result

    def delete_chat_sticker_set(self, chat_id: Union[(int, str)]) -> bool:
        """
        Use this method to delete a group sticker set from a supergroup. The bot must be an administrator in the chat
        for this to work and must have the appropriate admin rights. Use the field can_set_sticker_set
        optionally returned in getChat requests to check if the bot can use this method. Returns True on success.
        :param chat_id: Unique identifier for the target chat or username of the target supergroup
        (in the format @supergroupusername)
        :return:
        """
        result = apihelper.delete_chat_sticker_set(self.token, chat_id)
        return result

    def get_chat_member(self, chat_id: Union[(int, str)], user_id: int) -> types.ChatMember:
        """
        Use this method to get information about a member of a chat. Returns a ChatMember object on success.
        :param chat_id:
        :param user_id:
        :return:
        """
        result = apihelper.get_chat_member(self.token, chat_id, user_id)
        return types.ChatMember.de_json(result)

    def send_message--- This code section failed: ---

 L. 913         0  LOAD_FAST                'parse_mode'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                parse_mode
               12  JUMP_FORWARD         16  'to 16'
             14_0  COME_FROM             6  '6'
               14  LOAD_FAST                'parse_mode'
             16_0  COME_FROM            12  '12'
               16  STORE_FAST               'parse_mode'

 L. 915        18  LOAD_GLOBAL              types
               20  LOAD_ATTR                Message
               22  LOAD_METHOD              de_json

 L. 916        24  LOAD_GLOBAL              apihelper
               26  LOAD_METHOD              send_message

 L. 917        28  LOAD_FAST                'self'
               30  LOAD_ATTR                token
               32  LOAD_FAST                'chat_id'
               34  LOAD_FAST                'text'
               36  LOAD_FAST                'disable_web_page_preview'
               38  LOAD_FAST                'reply_to_message_id'

 L. 918        40  LOAD_FAST                'reply_markup'
               42  LOAD_FAST                'parse_mode'
               44  LOAD_FAST                'disable_notification'
               46  LOAD_FAST                'timeout'

 L. 919        48  LOAD_FAST                'entities'
               50  LOAD_FAST                'allow_sending_without_reply'

 L. 916        52  CALL_METHOD_11       11  ''

 L. 915        54  CALL_METHOD_1         1  ''
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def forward_message(self, chat_id: Union[(int, str)], from_chat_id: Union[(int, str)], message_id: int, disable_notification: Optional[bool]=None, timeout: Optional[int]=None) -> types.Message:
        """
        Use this method to forward messages of any kind.
        :param disable_notification:
        :param chat_id: which chat to forward
        :param from_chat_id: which chat message from
        :param message_id: message id
        :param timeout:
        :return: API reply.
        """
        return types.Message.de_json(apihelper.forward_message(self.token, chat_id, from_chat_id, message_id, disable_notification, timeout))

    def copy_message(self, chat_id: Union[(int, str)], from_chat_id: Union[(int, str)], message_id: int, caption: Optional[str]=None, parse_mode: Optional[str]=None, caption_entities: Optional[List[types.MessageEntity]]=None, disable_notification: Optional[bool]=None, reply_to_message_id: Optional[int]=None, allow_sending_without_reply: Optional[bool]=None, reply_markup: Optional[REPLY_MARKUP_TYPES]=None, timeout: Optional[int]=None) -> int:
        """
        Use this method to copy messages of any kind.
        :param chat_id: which chat to forward
        :param from_chat_id: which chat message from
        :param message_id: message id
        :param caption:
        :param parse_mode:
        :param caption_entities:
        :param disable_notification:
        :param reply_to_message_id:
        :param allow_sending_without_reply:
        :param reply_markup:
        :param timeout:
        :return: API reply.
        """
        return types.MessageID.de_json(apihelper.copy_message(self.token, chat_id, from_chat_id, message_id, caption, parse_mode, caption_entities, disable_notification, reply_to_message_id, allow_sending_without_reply, reply_markup, timeout))

    def delete_message(self, chat_id: Union[(int, str)], message_id: int, timeout: Optional[int]=None) -> bool:
        """
        Use this method to delete message. Returns True on success.
        :param chat_id: in which chat to delete
        :param message_id: which message to delete
        :param timeout:
        :return: API reply.
        """
        return apihelper.delete_message(self.token, chat_id, message_id, timeout)

    def send_dice(self, chat_id: Union[(int, str)], emoji: Optional[str]=None, disable_notification: Optional[bool]=None, reply_to_message_id: Optional[int]=None, reply_markup: Optional[REPLY_MARKUP_TYPES]=None, timeout: Optional[int]=None, allow_sending_without_reply: Optional[bool]=None) -> types.Message:
        """
        Use this method to send dices.
        :param chat_id:
        :param emoji:
        :param disable_notification:
        :param reply_to_message_id:
        :param reply_markup:
        :param timeout:
        :param allow_sending_without_reply:
        :return: Message
        """
        return types.Message.de_json(apihelper.send_dice(self.token, chat_id, emoji, disable_notification, reply_to_message_id, reply_markup, timeout, allow_sending_without_reply))

    def send_photo--- This code section failed: ---

 L.1026         0  LOAD_FAST                'parse_mode'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                parse_mode
               12  JUMP_FORWARD         16  'to 16'
             14_0  COME_FROM             6  '6'
               14  LOAD_FAST                'parse_mode'
             16_0  COME_FROM            12  '12'
               16  STORE_FAST               'parse_mode'

 L.1028        18  LOAD_GLOBAL              types
               20  LOAD_ATTR                Message
               22  LOAD_METHOD              de_json

 L.1029        24  LOAD_GLOBAL              apihelper
               26  LOAD_METHOD              send_photo

 L.1030        28  LOAD_FAST                'self'
               30  LOAD_ATTR                token
               32  LOAD_FAST                'chat_id'
               34  LOAD_FAST                'photo'
               36  LOAD_FAST                'caption'
               38  LOAD_FAST                'reply_to_message_id'
               40  LOAD_FAST                'reply_markup'

 L.1031        42  LOAD_FAST                'parse_mode'
               44  LOAD_FAST                'disable_notification'
               46  LOAD_FAST                'timeout'
               48  LOAD_FAST                'caption_entities'

 L.1032        50  LOAD_FAST                'allow_sending_without_reply'

 L.1029        52  CALL_METHOD_11       11  ''

 L.1028        54  CALL_METHOD_1         1  ''
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def send_audio--- This code section failed: ---

 L.1065         0  LOAD_FAST                'parse_mode'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                parse_mode
               12  JUMP_FORWARD         16  'to 16'
             14_0  COME_FROM             6  '6'
               14  LOAD_FAST                'parse_mode'
             16_0  COME_FROM            12  '12'
               16  STORE_FAST               'parse_mode'

 L.1067        18  LOAD_GLOBAL              types
               20  LOAD_ATTR                Message
               22  LOAD_METHOD              de_json

 L.1068        24  LOAD_GLOBAL              apihelper
               26  LOAD_METHOD              send_audio

 L.1069        28  LOAD_FAST                'self'
               30  LOAD_ATTR                token
               32  LOAD_FAST                'chat_id'
               34  LOAD_FAST                'audio'
               36  LOAD_FAST                'caption'
               38  LOAD_FAST                'duration'
               40  LOAD_FAST                'performer'
               42  LOAD_FAST                'title'
               44  LOAD_FAST                'reply_to_message_id'

 L.1070        46  LOAD_FAST                'reply_markup'
               48  LOAD_FAST                'parse_mode'
               50  LOAD_FAST                'disable_notification'
               52  LOAD_FAST                'timeout'
               54  LOAD_FAST                'thumb'

 L.1071        56  LOAD_FAST                'caption_entities'
               58  LOAD_FAST                'allow_sending_without_reply'

 L.1068        60  CALL_METHOD_15       15  ''

 L.1067        62  CALL_METHOD_1         1  ''
               64  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def send_voice--- This code section failed: ---

 L.1099         0  LOAD_FAST                'parse_mode'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                parse_mode
               12  JUMP_FORWARD         16  'to 16'
             14_0  COME_FROM             6  '6'
               14  LOAD_FAST                'parse_mode'
             16_0  COME_FROM            12  '12'
               16  STORE_FAST               'parse_mode'

 L.1101        18  LOAD_GLOBAL              types
               20  LOAD_ATTR                Message
               22  LOAD_METHOD              de_json

 L.1102        24  LOAD_GLOBAL              apihelper
               26  LOAD_METHOD              send_voice

 L.1103        28  LOAD_FAST                'self'
               30  LOAD_ATTR                token
               32  LOAD_FAST                'chat_id'
               34  LOAD_FAST                'voice'
               36  LOAD_FAST                'caption'
               38  LOAD_FAST                'duration'
               40  LOAD_FAST                'reply_to_message_id'
               42  LOAD_FAST                'reply_markup'

 L.1104        44  LOAD_FAST                'parse_mode'
               46  LOAD_FAST                'disable_notification'
               48  LOAD_FAST                'timeout'
               50  LOAD_FAST                'caption_entities'

 L.1105        52  LOAD_FAST                'allow_sending_without_reply'

 L.1102        54  CALL_METHOD_12       12  ''

 L.1101        56  CALL_METHOD_1         1  ''
               58  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def send_document--- This code section failed: ---

 L.1133         0  LOAD_FAST                'parse_mode'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                parse_mode
               12  JUMP_FORWARD         16  'to 16'
             14_0  COME_FROM             6  '6'
               14  LOAD_FAST                'parse_mode'
             16_0  COME_FROM            12  '12'
               16  STORE_FAST               'parse_mode'

 L.1135        18  LOAD_GLOBAL              types
               20  LOAD_ATTR                Message
               22  LOAD_METHOD              de_json

 L.1136        24  LOAD_GLOBAL              apihelper
               26  LOAD_METHOD              send_data

 L.1137        28  LOAD_FAST                'self'
               30  LOAD_ATTR                token
               32  LOAD_FAST                'chat_id'
               34  LOAD_FAST                'data'
               36  LOAD_STR                 'document'
               38  LOAD_FAST                'reply_to_message_id'
               40  LOAD_FAST                'reply_markup'

 L.1138        42  LOAD_FAST                'parse_mode'
               44  LOAD_FAST                'disable_notification'
               46  LOAD_FAST                'timeout'
               48  LOAD_FAST                'caption'
               50  LOAD_FAST                'thumb'
               52  LOAD_FAST                'caption_entities'

 L.1139        54  LOAD_FAST                'allow_sending_without_reply'

 L.1136        56  CALL_METHOD_13       13  ''

 L.1135        58  CALL_METHOD_1         1  ''
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def send_sticker(self, chat_id: Union[(int, str)], data: Union[(Any, str)], reply_to_message_id: Optional[int]=None, reply_markup: Optional[REPLY_MARKUP_TYPES]=None, disable_notification: Optional[bool]=None, timeout: Optional[int]=None, allow_sending_without_reply: Optional[bool]=None) -> types.Message:
        """
        Use this method to send .webp stickers.
        :param chat_id:
        :param data:
        :param reply_to_message_id:
        :param reply_markup:
        :param disable_notification: to disable the notification
        :param timeout: timeout
        :param allow_sending_without_reply:
        :return: API reply.
        """
        return types.Message.de_json(apihelper.send_data((self.token),
          chat_id=chat_id, data=data, data_type='sticker', reply_to_message_id=reply_to_message_id,
          reply_markup=reply_markup,
          disable_notification=disable_notification,
          timeout=timeout,
          allow_sending_without_reply=allow_sending_without_reply))

    def send_video--- This code section failed: ---

 L.1201         0  LOAD_FAST                'parse_mode'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                parse_mode
               12  JUMP_FORWARD         16  'to 16'
             14_0  COME_FROM             6  '6'
               14  LOAD_FAST                'parse_mode'
             16_0  COME_FROM            12  '12'
               16  STORE_FAST               'parse_mode'

 L.1203        18  LOAD_GLOBAL              types
               20  LOAD_ATTR                Message
               22  LOAD_METHOD              de_json

 L.1204        24  LOAD_GLOBAL              apihelper
               26  LOAD_METHOD              send_video

 L.1205        28  LOAD_FAST                'self'
               30  LOAD_ATTR                token
               32  LOAD_FAST                'chat_id'
               34  LOAD_FAST                'data'
               36  LOAD_FAST                'duration'
               38  LOAD_FAST                'caption'
               40  LOAD_FAST                'reply_to_message_id'
               42  LOAD_FAST                'reply_markup'

 L.1206        44  LOAD_FAST                'parse_mode'
               46  LOAD_FAST                'supports_streaming'
               48  LOAD_FAST                'disable_notification'
               50  LOAD_FAST                'timeout'
               52  LOAD_FAST                'thumb'
               54  LOAD_FAST                'width'
               56  LOAD_FAST                'height'

 L.1207        58  LOAD_FAST                'caption_entities'
               60  LOAD_FAST                'allow_sending_without_reply'

 L.1204        62  CALL_METHOD_16       16  ''

 L.1203        64  CALL_METHOD_1         1  ''
               66  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def send_animation--- This code section failed: ---

 L.1238         0  LOAD_FAST                'parse_mode'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                parse_mode
               12  JUMP_FORWARD         16  'to 16'
             14_0  COME_FROM             6  '6'
               14  LOAD_FAST                'parse_mode'
             16_0  COME_FROM            12  '12'
               16  STORE_FAST               'parse_mode'

 L.1240        18  LOAD_GLOBAL              types
               20  LOAD_ATTR                Message
               22  LOAD_METHOD              de_json

 L.1241        24  LOAD_GLOBAL              apihelper
               26  LOAD_METHOD              send_animation

 L.1242        28  LOAD_FAST                'self'
               30  LOAD_ATTR                token
               32  LOAD_FAST                'chat_id'
               34  LOAD_FAST                'animation'
               36  LOAD_FAST                'duration'
               38  LOAD_FAST                'caption'
               40  LOAD_FAST                'reply_to_message_id'

 L.1243        42  LOAD_FAST                'reply_markup'
               44  LOAD_FAST                'parse_mode'
               46  LOAD_FAST                'disable_notification'
               48  LOAD_FAST                'timeout'
               50  LOAD_FAST                'thumb'

 L.1244        52  LOAD_FAST                'caption_entities'
               54  LOAD_FAST                'allow_sending_without_reply'

 L.1241        56  CALL_METHOD_13       13  ''

 L.1240        58  CALL_METHOD_1         1  ''
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def send_video_note(self, chat_id: Union[(int, str)], data: Union[(Any, str)], duration: Optional[int]=None, length: Optional[int]=None, reply_to_message_id: Optional[int]=None, reply_markup: Optional[REPLY_MARKUP_TYPES]=None, disable_notification: Optional[bool]=None, timeout: Optional[int]=None, thumb: Optional[Union[(Any, str)]]=None, allow_sending_without_reply: Optional[bool]=None) -> types.Message:
        """
        As of v.4.0, Telegram clients support rounded square mp4 videos of up to 1 minute long. Use this method to send
            video messages.
        :param chat_id: Integer : Unique identifier for the message recipient — User or GroupChat id
        :param data: InputFile or String : Video note to send. You can either pass a file_id as String to resend
            a video that is already on the Telegram server
        :param duration: Integer : Duration of sent video in seconds
        :param length: Integer : Video width and height, Can't be None and should be in range of (0, 640)
        :param reply_to_message_id:
        :param reply_markup:
        :param disable_notification:
        :param timeout:
        :param thumb: InputFile or String : Thumbnail of the file sent
        :param allow_sending_without_reply:
        :return:
        """
        return types.Message.de_json(apihelper.send_video_noteself.tokenchat_iddatadurationlengthreply_to_message_idreply_markupdisable_notificationtimeoutthumballow_sending_without_reply)

    def send_media_group(self, chat_id: Union[(int, str)], media: List[Union[(
 types.InputMediaAudio, types.InputMediaDocument,
 types.InputMediaPhoto, types.InputMediaVideo)]], disable_notification: Optional[bool]=None, reply_to_message_id: Optional[int]=None, timeout: Optional[int]=None, allow_sending_without_reply: Optional[bool]=None) -> List[types.Message]:
        """
        send a group of photos or videos as an album. On success, an array of the sent Messages is returned.
        :param chat_id:
        :param media:
        :param disable_notification:
        :param reply_to_message_id:
        :param timeout:
        :param allow_sending_without_reply:
        :return:
        """
        result = apihelper.send_media_group(self.token, chat_id, media, disable_notification, reply_to_message_id, timeout, allow_sending_without_reply)
        ret = []
        for msg in result:
            ret.append(types.Message.de_json(msg))
        else:
            return ret

    def send_location(self, chat_id: Union[(int, str)], latitude: float, longitude: float, live_period: Optional[int]=None, reply_to_message_id: Optional[int]=None, reply_markup: Optional[REPLY_MARKUP_TYPES]=None, disable_notification: Optional[bool]=None, timeout: Optional[int]=None, horizontal_accuracy: Optional[float]=None, heading: Optional[int]=None, proximity_alert_radius: Optional[int]=None, allow_sending_without_reply: Optional[bool]=None) -> types.Message:
        """
        Use this method to send point on the map.
        :param chat_id:
        :param latitude:
        :param longitude:
        :param live_period:
        :param reply_to_message_id:
        :param reply_markup:
        :param disable_notification:
        :param timeout:
        :param horizontal_accuracy:
        :param heading:
        :param proximity_alert_radius:
        :param allow_sending_without_reply:
        :return: API reply.
        """
        return types.Message.de_json(apihelper.send_locationself.tokenchat_idlatitudelongitudelive_periodreply_to_message_idreply_markupdisable_notificationtimeouthorizontal_accuracyheadingproximity_alert_radiusallow_sending_without_reply)

    def edit_message_live_location(self, latitude: float, longitude: float, chat_id: Optional[Union[(int, str)]]=None, message_id: Optional[int]=None, inline_message_id: Optional[str]=None, reply_markup: Optional[REPLY_MARKUP_TYPES]=None, timeout: Optional[int]=None, horizontal_accuracy: Optional[float]=None, heading: Optional[int]=None, proximity_alert_radius: Optional[int]=None) -> types.Message:
        """
        Use this method to edit live location
        :param latitude:
        :param longitude:
        :param chat_id:
        :param message_id:
        :param reply_markup:
        :param timeout:
        :param inline_message_id:
        :param horizontal_accuracy:
        :param heading:
        :param proximity_alert_radius:
        :return:
        """
        return types.Message.de_json(apihelper.edit_message_live_locationself.tokenlatitudelongitudechat_idmessage_idinline_message_idreply_markuptimeouthorizontal_accuracyheadingproximity_alert_radius)

    def stop_message_live_location(self, chat_id: Optional[Union[(int, str)]]=None, message_id: Optional[int]=None, inline_message_id: Optional[str]=None, reply_markup: Optional[REPLY_MARKUP_TYPES]=None, timeout: Optional[int]=None) -> types.Message:
        """
        Use this method to stop updating a live location message sent by the bot
        or via the bot (for inline bots) before live_period expires
        :param chat_id:
        :param message_id:
        :param inline_message_id:
        :param reply_markup:
        :param timeout:
        :return:
        """
        return types.Message.de_json(apihelper.stop_message_live_location(self.token, chat_id, message_id, inline_message_id, reply_markup, timeout))

    def send_venue(self, chat_id: Union[(int, str)], latitude: float, longitude: float, title: str, address: str, foursquare_id: Optional[str]=None, foursquare_type: Optional[str]=None, disable_notification: Optional[bool]=None, reply_to_message_id: Optional[int]=None, reply_markup: Optional[REPLY_MARKUP_TYPES]=None, timeout: Optional[int]=None, allow_sending_without_reply: Optional[bool]=None, google_place_id: Optional[str]=None, google_place_type: Optional[str]=None) -> types.Message:
        """
        Use this method to send information about a venue.
        :param chat_id: Integer or String : Unique identifier for the target chat or username of the target channel
        :param latitude: Float : Latitude of the venue
        :param longitude: Float : Longitude of the venue
        :param title: String : Name of the venue
        :param address: String : Address of the venue
        :param foursquare_id: String : Foursquare identifier of the venue
        :param foursquare_type: Foursquare type of the venue, if known. (For example, “arts_entertainment/default”,
            “arts_entertainment/aquarium” or “food/icecream”.)
        :param disable_notification:
        :param reply_to_message_id:
        :param reply_markup:
        :param timeout:
        :param allow_sending_without_reply:
        :param google_place_id:
        :param google_place_type:
        :return:
        """
        return types.Message.de_json(apihelper.send_venueself.tokenchat_idlatitudelongitudetitleaddressfoursquare_idfoursquare_typedisable_notificationreply_to_message_idreply_markuptimeoutallow_sending_without_replygoogle_place_idgoogle_place_type)

    def send_contact(self, chat_id: Union[(int, str)], phone_number: str, first_name: str, last_name: Optional[str]=None, vcard: Optional[str]=None, disable_notification: Optional[bool]=None, reply_to_message_id: Optional[int]=None, reply_markup: Optional[REPLY_MARKUP_TYPES]=None, timeout: Optional[int]=None, allow_sending_without_reply: Optional[bool]=None) -> types.Message:
        return types.Message.de_json(apihelper.send_contactself.tokenchat_idphone_numberfirst_namelast_namevcarddisable_notificationreply_to_message_idreply_markuptimeoutallow_sending_without_reply)

    def send_chat_action(self, chat_id: Union[(int, str)], action: str, timeout: Optional[int]=None) -> bool:
        """
        Use this method when you need to tell the user that something is happening on the bot's side.
        The status is set for 5 seconds or less (when a message arrives from your bot, Telegram clients clear
        its typing status).
        :param chat_id:
        :param action:  One of the following strings: 'typing', 'upload_photo', 'record_video', 'upload_video',
                        'record_audio', 'upload_audio', 'upload_document', 'find_location', 'record_video_note',
                        'upload_video_note'.
        :param timeout:
        :return: API reply. :type: boolean
        """
        return apihelper.send_chat_action(self.token, chat_id, action, timeout)

    def kick_chat_member(self, chat_id: Union[(int, str)], user_id: int, until_date: Optional[Union[(int, datetime)]]=None, revoke_messages: Optional[bool]=None) -> bool:
        """
        Use this method to kick a user from a group or a supergroup.
        :param chat_id: Int or string : Unique identifier for the target group or username of the target supergroup
        :param user_id: Int : Unique identifier of the target user
        :param until_date: Date when the user will be unbanned, unix time. If user is banned for more than 366 days or
               less than 30 seconds from the current time they are considered to be banned forever
        :param revoke_messages: Bool: Pass True to delete all messages from the chat for the user that is being removed.
                If False, the user will be able to see messages in the group that were sent before the user was removed. 
                Always True for supergroups and channels.
        :return: boolean
        """
        return apihelper.kick_chat_member(self.token, chat_id, user_id, until_date, revoke_messages)

    def unban_chat_member(self, chat_id: Union[(int, str)], user_id: int, only_if_banned: Optional[bool]=False) -> bool:
        """
        Use this method to unban a previously kicked user in a supergroup or channel.
        The user will not return to the group or channel automatically, but will be able to join via link, etc.
        The bot must be an administrator for this to work. By default, this method guarantees that after the call
        the user is not a member of the chat, but will be able to join it. So if the user is a member of the chat
        they will also be removed from the chat. If you don't want this, use the parameter only_if_banned.

        :param chat_id: Unique identifier for the target group or username of the target supergroup or channel
            (in the format @username)
        :param user_id: Unique identifier of the target user
        :param only_if_banned: Do nothing if the user is not banned
        :return: True on success
        """
        return apihelper.unban_chat_member(self.token, chat_id, user_id, only_if_banned)

    def restrict_chat_member(self, chat_id: Union[(int, str)], user_id: int, until_date: Optional[Union[(int, datetime)]]=None, can_send_messages: Optional[bool]=None, can_send_media_messages: Optional[bool]=None, can_send_polls: Optional[bool]=None, can_send_other_messages: Optional[bool]=None, can_add_web_page_previews: Optional[bool]=None, can_change_info: Optional[bool]=None, can_invite_users: Optional[bool]=None, can_pin_messages: Optional[bool]=None) -> bool:
        """
        Use this method to restrict a user in a supergroup.
        The bot must be an administrator in the supergroup for this to work and must have
        the appropriate admin rights. Pass True for all boolean parameters to lift restrictions from a user.

        :param chat_id: Int or String :         Unique identifier for the target group or username of the target supergroup
            or channel (in the format @channelusername)
        :param user_id: Int : Unique identifier of the target user
        :param until_date: Date when restrictions will be lifted for the user, unix time.
            If user is restricted for more than 366 days or less than 30 seconds from the current time,
            they are considered to be restricted forever
        :param can_send_messages: Pass True, if the user can send text messages, contacts, locations and venues
        :param can_send_media_messages Pass True, if the user can send audios, documents, photos, videos, video notes
            and voice notes, implies can_send_messages
        :param can_send_polls: Pass True, if the user is allowed to send polls, implies can_send_messages
        :param can_send_other_messages: Pass True, if the user can send animations, games, stickers and
            use inline bots, implies can_send_media_messages
        :param can_add_web_page_previews: Pass True, if the user may add web page previews to their messages,
            implies can_send_media_messages
        :param can_change_info: Pass True, if the user is allowed to change the chat title, photo and other settings.
            Ignored in public supergroups
        :param can_invite_users: Pass True, if the user is allowed to invite new users to the chat,
            implies can_invite_users
        :param can_pin_messages: Pass True, if the user is allowed to pin messages. Ignored in public supergroups
        :return: True on success
        """
        return apihelper.restrict_chat_member(self.token, chat_id, user_id, until_date, can_send_messages, can_send_media_messages, can_send_polls, can_send_other_messages, can_add_web_page_previews, can_change_info, can_invite_users, can_pin_messages)

    def promote_chat_member(self, chat_id: Union[(int, str)], user_id: int, can_change_info: Optional[bool]=None, can_post_messages: Optional[bool]=None, can_edit_messages: Optional[bool]=None, can_delete_messages: Optional[bool]=None, can_invite_users: Optional[bool]=None, can_restrict_members: Optional[bool]=None, can_pin_messages: Optional[bool]=None, can_promote_members: Optional[bool]=None, is_anonymous: Optional[bool]=None, can_manage_chat: Optional[bool]=None, can_manage_voice_chats: Optional[bool]=None) -> bool:
        """
        Use this method to promote or demote a user in a supergroup or a channel. The bot must be an administrator
        in the chat for this to work and must have the appropriate admin rights.
        Pass False for all boolean parameters to demote a user.

        :param chat_id: Unique identifier for the target chat or username of the target channel (
            in the format @channelusername)
        :param user_id: Int : Unique identifier of the target user
        :param can_change_info: Bool: Pass True, if the administrator can change chat title, photo and other settings
        :param can_post_messages: Bool : Pass True, if the administrator can create channel posts, channels only
        :param can_edit_messages: Bool : Pass True, if the administrator can edit messages of other users, channels only
        :param can_delete_messages: Bool : Pass True, if the administrator can delete messages of other users
        :param can_invite_users: Bool : Pass True, if the administrator can invite new users to the chat
        :param can_restrict_members: Bool: Pass True, if the administrator can restrict, ban or unban chat members
        :param can_pin_messages: Bool: Pass True, if the administrator can pin messages, supergroups only
        :param can_promote_members: Bool: Pass True, if the administrator can add new administrators with a subset
            of his own privileges or demote administrators that he has promoted, directly or indirectly
            (promoted by administrators that were appointed by him)
        :param is_anonymous: Bool: Pass True, if the administrator's presence in the chat is hidden
        :param can_manage_chat: Bool: Pass True, if the administrator can access the chat event log, chat statistics, 
            message statistics in channels, see channel members, 
            see anonymous administrators in supergroups and ignore slow mode. 
            Implied by any other administrator privilege
        :param can_manage_voice_chats: Bool: Pass True, if the administrator can manage voice chats
            For now, bots can use this privilege only for passing to other administrators.
        :return: True on success.
        """
        return apihelper.promote_chat_member(self.token, chat_id, user_id, can_change_info, can_post_messages, can_edit_messages, can_delete_messages, can_invite_users, can_restrict_members, can_pin_messages, can_promote_members, is_anonymous, can_manage_chat, can_manage_voice_chats)

    def set_chat_administrator_custom_title(self, chat_id: Union[(int, str)], user_id: int, custom_title: str) -> bool:
        """
        Use this method to set a custom title for an administrator
        in a supergroup promoted by the bot.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup
            (in the format @supergroupusername)
        :param user_id: Unique identifier of the target user
        :param custom_title: New custom title for the administrator;
            0-16 characters, emoji are not allowed
        :return: True on success.
        """
        return apihelper.set_chat_administrator_custom_title(self.token, chat_id, user_id, custom_title)

    def set_chat_permissions(self, chat_id: Union[(int, str)], permissions: types.ChatPermissions) -> bool:
        """
        Use this method to set default chat permissions for all members.
        The bot must be an administrator in the group or a supergroup for this to work
        and must have the can_restrict_members admin rights.

        :param chat_id: Unique identifier for the target chat or username of the target supergroup
            (in the format @supergroupusername)
        :param permissions: New default chat permissions
        :return: True on success
        """
        return apihelper.set_chat_permissions(self.token, chat_id, permissions)

    def create_chat_invite_link(self, chat_id: Union[(int, str)], expire_date: Optional[Union[(int, datetime)]]=None, member_limit: Optional[int]=None) -> types.ChatInviteLink:
        """
        Use this method to create an additional invite link for a chat.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.

        :param chat_id: Id: Unique identifier for the target chat or username of the target channel
            (in the format @channelusername)
        :expire_date: Point in time (Unix timestamp) when the link will expire
        :member_limit: Maximum number of users that can be members of the chat simultaneously
        :return:
        """
        return types.ChatInviteLink.de_json(apihelper.create_chat_invite_link(self.token, chat_id, expire_date, member_limit))

    def edit_chat_invite_link(self, chat_id: Union[(int, str)], invite_link: str, expire_date: Optional[Union[(int, datetime)]]=None, member_limit: Optional[int]=None) -> types.ChatInviteLink:
        """
        Use this method to edit a non-primary invite link created by the bot.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.

        :param chat_id: Id: Unique identifier for the target chat or username of the target channel
            (in the format @channelusername)
        :invite_link: The invite link to edit
        :expire_date: Point in time (Unix timestamp) when the link will expire
        :member_limit: Maximum number of users that can be members of the chat simultaneously
        :return:
        """
        return types.ChatInviteLink.de_json(apihelper.edit_chat_invite_link(self.token, chat_id, invite_link, expire_date, member_limit))

    def revoke_chat_invite_link(self, chat_id: Union[(int, str)], invite_link: str) -> types.ChatInviteLink:
        """
        Use this method to revoke an invite link created by the bot.
        Note: If the primary link is revoked, a new link is automatically generated The bot must be an administrator 
            in the chat for this to work and must have the appropriate admin rights.

        :param chat_id: Id: Unique identifier for the target chat or username of the target channel
            (in the format @channelusername)
        :invite_link: The invite link to revoke
        :return:
        """
        return types.ChatInviteLink.de_json(apihelper.revoke_chat_invite_link(self.token, chat_id, invite_link))

    def export_chat_invite_link(self, chat_id: Union[(int, str)]) -> str:
        """
        Use this method to export an invite link to a supergroup or a channel. The bot must be an administrator
        in the chat for this to work and must have the appropriate admin rights.

        :param chat_id: Id: Unique identifier for the target chat or username of the target channel
            (in the format @channelusername)
        :return: exported invite link as String on success.
        """
        return apihelper.export_chat_invite_link(self.token, chat_id)

    def set_chat_photo(self, chat_id: Union[(int, str)], photo: Any) -> bool:
        """
        Use this method to set a new profile photo for the chat. Photos can't be changed for private chats.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.
        Returns True on success.
        Note: In regular groups (non-supergroups), this method will only work if the ‘All Members Are Admins’
            setting is off in the target group.
        :param chat_id: Int or Str: Unique identifier for the target chat or username of the target channel
            (in the format @channelusername)
        :param photo: InputFile: New chat photo, uploaded using multipart/form-data
        :return:
        """
        return apihelper.set_chat_photo(self.token, chat_id, photo)

    def delete_chat_photo(self, chat_id: Union[(int, str)]) -> bool:
        """
        Use this method to delete a chat photo. Photos can't be changed for private chats.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.
        Returns True on success.
        Note: In regular groups (non-supergroups), this method will only work if the ‘All Members Are Admins’
            setting is off in the target group.
        :param chat_id: Int or Str: Unique identifier for the target chat or username of the target channel
            (in the format @channelusername)
        :return:
        """
        return apihelper.delete_chat_photo(self.token, chat_id)

    def get_my_commands(self, scope: Optional[Union[(
 types.BotCommandScopeDefault, types.BotCommandScopeAllPrivateChats,
 types.BotCommandScopeAllGroupChats, types.BotCommandScopeAllChatAdministrators,
 types.BotCommandScopeChat,
 types.BotCommandScopeChatAdministrators, types.BotCommandScopeChatMember)]]=None, language_code: Optional[str]=None) -> List[types.BotCommand]:
        """
        Use this method to get the current list of the bot's commands for the given scope and user language
        :param scope: scope of users for which the commands are relevant
        :param language_code: A two-letter ISO 639-1 language code
        Returns List of BotCommand on success.
        """
        result = apihelper.get_my_commands(self.token, scope, language_code)
        return [types.BotCommand.de_json(cmd) for cmd in result]

    def set_my_commands(self, commands: List[types.BotCommand], scope: Optional[Union[(
 types.BotCommandScopeDefault, types.BotCommandScopeAllPrivateChats,
 types.BotCommandScopeAllGroupChats, types.BotCommandScopeAllChatAdministrators,
 types.BotCommandScopeChat,
 types.BotCommandScopeChatAdministrators, types.BotCommandScopeChatMember)]]=None, language_code: Optional[str]=None) -> bool:
        """
        Use this method to change the list of the bot's commands.
        :param commands: List of BotCommand. At most 100 commands can be specified.
        :param scope: scope of users for which the commands are relevant
        :param language_code: A two-letter ISO 639-1 language code
        :return:
        """
        return apihelper.set_my_commands(self.token, commands, scope, language_code)

    def delete_my_commands(self, scope: Optional[Union[(
 types.BotCommandScopeDefault, types.BotCommandScopeAllPrivateChats,
 types.BotCommandScopeAllGroupChats, types.BotCommandScopeAllChatAdministrators,
 types.BotCommandScopeChat,
 types.BotCommandScopeChatAdministrators, types.BotCommandScopeChatMember)]]=None, language_code: Optional[str]=None) -> bool:
        """
        Use this method to delete the list of the bot's commands for the given scope and user language.
        :param scope: scope of users for which the commands are relevant
        :param language_code: A two-letter ISO 639-1 language code
        :return:
        """
        return apihelper.delete_my_commands(self.token, scope, language_code)

    def set_chat_title(self, chat_id: Union[(int, str)], title: str) -> bool:
        """
        Use this method to change the title of a chat. Titles can't be changed for private chats.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.
        Returns True on success.
        Note: In regular groups (non-supergroups), this method will only work if the ‘All Members Are Admins’
            setting is off in the target group.
        :param chat_id: Int or Str: Unique identifier for the target chat or username of the target channel
            (in the format @channelusername)
        :param title: New chat title, 1-255 characters
        :return:
        """
        return apihelper.set_chat_title(self.token, chat_id, title)

    def set_chat_description(self, chat_id: Union[(int, str)], description: Optional[str]=None) -> bool:
        """
        Use this method to change the description of a supergroup or a channel.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.

        :param chat_id: Int or Str: Unique identifier for the target chat or username of the target channel
            (in the format @channelusername)
        :param description: Str: New chat description, 0-255 characters
        :return: True on success.
        """
        return apihelper.set_chat_description(self.token, chat_id, description)

    def pin_chat_message(self, chat_id: Union[(int, str)], message_id: int, disable_notification: Optional[bool]=False) -> bool:
        """
        Use this method to pin a message in a supergroup.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.
        Returns True on success.
        :param chat_id: Int or Str: Unique identifier for the target chat or username of the target channel
            (in the format @channelusername)
        :param message_id: Int: Identifier of a message to pin
        :param disable_notification: Bool: Pass True, if it is not necessary to send a notification
            to all group members about the new pinned message
        :return:
        """
        return apihelper.pin_chat_message(self.token, chat_id, message_id, disable_notification)

    def unpin_chat_message(self, chat_id: Union[(int, str)], message_id: Optional[int]=None) -> bool:
        """
        Use this method to unpin specific pinned message in a supergroup chat.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.
        Returns True on success.
        :param chat_id: Int or Str: Unique identifier for the target chat or username of the target channel
            (in the format @channelusername)
        :param message_id: Int: Identifier of a message to unpin
        :return:
        """
        return apihelper.unpin_chat_message(self.token, chat_id, message_id)

    def unpin_all_chat_messages(self, chat_id: Union[(int, str)]) -> bool:
        """
        Use this method to unpin a all pinned messages in a supergroup chat.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.
        Returns True on success.
        :param chat_id: Int or Str: Unique identifier for the target chat or username of the target channel
            (in the format @channelusername)
        :return:
        """
        return apihelper.unpin_all_chat_messages(self.token, chat_id)

    def edit_message_text--- This code section failed: ---

 L.1837         0  LOAD_FAST                'parse_mode'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                parse_mode
               12  JUMP_FORWARD         16  'to 16'
             14_0  COME_FROM             6  '6'
               14  LOAD_FAST                'parse_mode'
             16_0  COME_FROM            12  '12'
               16  STORE_FAST               'parse_mode'

 L.1839        18  LOAD_GLOBAL              apihelper
               20  LOAD_METHOD              edit_message_text
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                token
               26  LOAD_FAST                'text'
               28  LOAD_FAST                'chat_id'
               30  LOAD_FAST                'message_id'
               32  LOAD_FAST                'inline_message_id'
               34  LOAD_FAST                'parse_mode'

 L.1840        36  LOAD_FAST                'disable_web_page_preview'
               38  LOAD_FAST                'reply_markup'

 L.1839        40  CALL_METHOD_8         8  ''
               42  STORE_FAST               'result'

 L.1841        44  LOAD_GLOBAL              type
               46  LOAD_FAST                'result'
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_GLOBAL              bool
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    60  'to 60'

 L.1842        56  LOAD_FAST                'result'
               58  RETURN_VALUE     
             60_0  COME_FROM            54  '54'

 L.1843        60  LOAD_GLOBAL              types
               62  LOAD_ATTR                Message
               64  LOAD_METHOD              de_json
               66  LOAD_FAST                'result'
               68  CALL_METHOD_1         1  ''
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def edit_message_media(self, media: Any, chat_id: Optional[Union[(int, str)]]=None, message_id: Optional[int]=None, inline_message_id: Optional[str]=None, reply_markup: Optional[REPLY_MARKUP_TYPES]=None) -> Union[(types.Message, bool)]:
        """
        Use this method to edit animation, audio, document, photo, or video messages.
        If a message is a part of a message album, then it can be edited only to a photo or a video.
        Otherwise, message type can be changed arbitrarily. When inline message is edited, new file can't be uploaded.
        Use previously uploaded file via its file_id or specify a URL.
        :param media:
        :param chat_id:
        :param message_id:
        :param inline_message_id:
        :param reply_markup:
        :return:
        """
        result = apihelper.edit_message_media(self.token, media, chat_id, message_id, inline_message_id, reply_markup)
        if type(result) == bool:
            return result
        return types.Message.de_json(result)

    def edit_message_reply_markup(self, chat_id: Optional[Union[(int, str)]]=None, message_id: Optional[int]=None, inline_message_id: Optional[str]=None, reply_markup: Optional[REPLY_MARKUP_TYPES]=None) -> Union[(types.Message, bool)]:
        """
        Use this method to edit only the reply markup of messages.
        :param chat_id:
        :param message_id:
        :param inline_message_id:
        :param reply_markup:
        :return:
        """
        result = apihelper.edit_message_reply_markup(self.token, chat_id, message_id, inline_message_id, reply_markup)
        if type(result) == bool:
            return result
        return types.Message.de_json(result)

    def send_game(self, chat_id: Union[(int, str)], game_short_name: str, disable_notification: Optional[bool]=None, reply_to_message_id: Optional[int]=None, reply_markup: Optional[REPLY_MARKUP_TYPES]=None, timeout: Optional[int]=None, allow_sending_without_reply: Optional[bool]=None) -> types.Message:
        """
        Used to send the game
        :param chat_id:
        :param game_short_name:
        :param disable_notification:
        :param reply_to_message_id:
        :param reply_markup:
        :param timeout:
        :param allow_sending_without_reply:
        :return:
        """
        result = apihelper.send_game(self.token, chat_id, game_short_name, disable_notification, reply_to_message_id, reply_markup, timeout, allow_sending_without_reply)
        return types.Message.de_json(result)

    def set_game_score(self, user_id: Union[(int, str)], score: int, force: Optional[bool]=None, chat_id: Optional[Union[(int, str)]]=None, message_id: Optional[int]=None, inline_message_id: Optional[str]=None, disable_edit_message: Optional[bool]=None) -> Union[(types.Message, bool)]:
        """
        Sets the value of points in the game to a specific user
        :param user_id:
        :param score:
        :param force:
        :param chat_id:
        :param message_id:
        :param inline_message_id:
        :param disable_edit_message:
        :return:
        """
        result = apihelper.set_game_score(self.token, user_id, score, force, disable_edit_message, chat_id, message_id, inline_message_id)
        if type(result) == bool:
            return result
        return types.Message.de_json(result)

    def get_game_high_scores(self, user_id: int, chat_id: Optional[Union[(int, str)]]=None, message_id: Optional[int]=None, inline_message_id: Optional[str]=None) -> List[types.GameHighScore]:
        """
        Gets top points and game play
        :param user_id:
        :param chat_id:
        :param message_id:
        :param inline_message_id:
        :return:
        """
        result = apihelper.get_game_high_scores(self.token, user_id, chat_id, message_id, inline_message_id)
        ret = []
        for r in result:
            ret.append(types.GameHighScore.de_json(r))
        else:
            return ret

    def send_invoice(self, chat_id: Union[(int, str)], title: str, description: str, invoice_payload: str, provider_token: str, currency: str, prices: List[types.LabeledPrice], start_parameter: Optional[str]=None, photo_url: Optional[str]=None, photo_size: Optional[int]=None, photo_width: Optional[int]=None, photo_height: Optional[int]=None, need_name: Optional[bool]=None, need_phone_number: Optional[bool]=None, need_email: Optional[bool]=None, need_shipping_address: Optional[bool]=None, send_phone_number_to_provider: Optional[bool]=None, send_email_to_provider: Optional[bool]=None, is_flexible: Optional[bool]=None, disable_notification: Optional[bool]=None, reply_to_message_id: Optional[int]=None, reply_markup: Optional[REPLY_MARKUP_TYPES]=None, provider_data: Optional[str]=None, timeout: Optional[int]=None, allow_sending_without_reply: Optional[bool]=None) -> types.Message:
        """
        Sends invoice
        :param chat_id: Unique identifier for the target private chat
        :param title: Product name
        :param description: Product description
        :param invoice_payload: Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user,
            use for your internal processes.
        :param provider_token: Payments provider token, obtained via @Botfather
        :param currency: Three-letter ISO 4217 currency code,
            see https://core.telegram.org/bots/payments#supported-currencies
        :param prices: Price breakdown, a list of components
            (e.g. product price, tax, discount, delivery cost, delivery tax, bonus, etc.)
        :param start_parameter: Unique deep-linking parameter that can be used to generate this invoice
            when used as a start parameter
        :param photo_url: URL of the product photo for the invoice. Can be a photo of the goods
            or a marketing image for a service. People like it better when they see what they are paying for.
        :param photo_size: Photo size
        :param photo_width: Photo width
        :param photo_height: Photo height
        :param need_name: Pass True, if you require the user's full name to complete the order
        :param need_phone_number: Pass True, if you require the user's phone number to complete the order
        :param need_email: Pass True, if you require the user's email to complete the order
        :param need_shipping_address: Pass True, if you require the user's shipping address to complete the order
        :param is_flexible: Pass True, if the final price depends on the shipping method
        :param send_phone_number_to_provider: Pass True, if user's phone number should be sent to provider
        :param send_email_to_provider: Pass True, if user's email address should be sent to provider
        :param disable_notification: Sends the message silently. Users will receive a notification with no sound.
        :param reply_to_message_id: If the message is a reply, ID of the original message
        :param reply_markup: A JSON-serialized object for an inline keyboard. If empty,
            one 'Pay total price' button will be shown. If not empty, the first button must be a Pay button
        :param provider_data: A JSON-serialized data about the invoice, which will be shared with the payment provider.
            A detailed description of required fields should be provided by the payment provider.
        :param timeout:
        :param allow_sending_without_reply:
        :return:
        """
        result = apihelper.send_invoice(self.token, chat_id, title, description, invoice_payload, provider_token, currency, prices, start_parameter, photo_url, photo_size, photo_width, photo_height, need_name, need_phone_number, need_email, need_shipping_address, send_phone_number_to_provider, send_email_to_provider, is_flexible, disable_notification, reply_to_message_id, reply_markup, provider_data, timeout, allow_sending_without_reply)
        return types.Message.de_json(result)

    def send_poll(self, chat_id: Union[(int, str)], question: str, options: List[str], is_anonymous: Optional[bool]=None, type: Optional[str]=None, allows_multiple_answers: Optional[bool]=None, correct_option_id: Optional[int]=None, explanation: Optional[str]=None, explanation_parse_mode: Optional[str]=None, open_period: Optional[int]=None, close_date: Optional[Union[(int, datetime)]]=None, is_closed: Optional[bool]=None, disable_notifications: Optional[bool]=False, reply_to_message_id: Optional[int]=None, reply_markup: Optional[REPLY_MARKUP_TYPES]=None, allow_sending_without_reply: Optional[bool]=None, timeout: Optional[int]=None, explanation_entities: Optional[List[types.MessageEntity]]=None) -> types.Message:
        """
        Send polls
        :param chat_id:
        :param question:
        :param options: array of str with answers
        :param is_anonymous:
        :param type:
        :param allows_multiple_answers:
        :param correct_option_id:
        :param explanation:
        :param explanation_parse_mode:
        :param open_period:
        :param close_date:
        :param is_closed:
        :param disable_notifications:
        :param reply_to_message_id:
        :param allow_sending_without_reply:
        :param reply_markup:
        :param timeout:
        :param explanation_entities:
        :return:
        """
        if isinstance(question, types.Poll):
            raise RuntimeError('The send_poll signature was changed, please see send_poll function details.')
        return types.Message.de_json(apihelper.send_poll(self.token, chat_id, question, options, is_anonymous, type, allows_multiple_answers, correct_option_id, explanation, explanation_parse_mode, open_period, close_date, is_closed, disable_notifications, reply_to_message_id, allow_sending_without_reply, reply_markup, timeout, explanation_entities))

    def stop_poll(self, chat_id: Union[(int, str)], message_id: int, reply_markup: Optional[REPLY_MARKUP_TYPES]=None) -> types.Poll:
        """
        Stops poll
        :param chat_id:
        :param message_id:
        :param reply_markup:
        :return:
        """
        return types.Poll.de_json(apihelper.stop_poll(self.token, chat_id, message_id, reply_markup))

    def answer_shipping_query(self, shipping_query_id: str, ok: bool, shipping_options: Optional[List[types.ShippingOption]]=None, error_message: Optional[str]=None) -> bool:
        """
        Asks for an answer to a shipping question
        :param shipping_query_id:
        :param ok:
        :param shipping_options:
        :param error_message:
        :return:
        """
        return apihelper.answer_shipping_query(self.token, shipping_query_id, ok, shipping_options, error_message)

    def answer_pre_checkout_query(self, pre_checkout_query_id: int, ok: bool, error_message: Optional[str]=None) -> bool:
        """
        Response to a request for pre-inspection
        :param pre_checkout_query_id:
        :param ok:
        :param error_message:
        :return:
        """
        return apihelper.answer_pre_checkout_query(self.token, pre_checkout_query_id, ok, error_message)

    def edit_message_caption--- This code section failed: ---

 L.2117         0  LOAD_FAST                'parse_mode'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                parse_mode
               12  JUMP_FORWARD         16  'to 16'
             14_0  COME_FROM             6  '6'
               14  LOAD_FAST                'parse_mode'
             16_0  COME_FROM            12  '12'
               16  STORE_FAST               'parse_mode'

 L.2119        18  LOAD_GLOBAL              apihelper
               20  LOAD_METHOD              edit_message_caption
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                token
               26  LOAD_FAST                'caption'
               28  LOAD_FAST                'chat_id'
               30  LOAD_FAST                'message_id'
               32  LOAD_FAST                'inline_message_id'

 L.2120        34  LOAD_FAST                'parse_mode'
               36  LOAD_FAST                'reply_markup'

 L.2119        38  CALL_METHOD_7         7  ''
               40  STORE_FAST               'result'

 L.2121        42  LOAD_GLOBAL              type
               44  LOAD_FAST                'result'
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_GLOBAL              bool
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    58  'to 58'

 L.2122        54  LOAD_FAST                'result'
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L.2123        58  LOAD_GLOBAL              types
               60  LOAD_ATTR                Message
               62  LOAD_METHOD              de_json
               64  LOAD_FAST                'result'
               66  CALL_METHOD_1         1  ''
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def reply_to--- This code section failed: ---

 L.2133         0  LOAD_FAST                'self'
                2  LOAD_ATTR                send_message
                4  LOAD_FAST                'message'
                6  LOAD_ATTR                chat
                8  LOAD_ATTR                id
               10  LOAD_FAST                'text'
               12  BUILD_TUPLE_2         2 
               14  LOAD_STR                 'reply_to_message_id'
               16  LOAD_FAST                'message'
               18  LOAD_ATTR                message_id
               20  BUILD_MAP_1           1 
               22  LOAD_FAST                'kwargs'
               24  <164>                 1  ''
               26  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               28  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def answer_inline_query(self, inline_query_id: str, results: List[Any], cache_time: Optional[int]=None, is_personal: Optional[bool]=None, next_offset: Optional[str]=None, switch_pm_text: Optional[str]=None, switch_pm_parameter: Optional[str]=None) -> bool:
        """
        Use this method to send answers to an inline query. On success, True is returned.
        No more than 50 results per query are allowed.
        :param inline_query_id: Unique identifier for the answered query
        :param results: Array of results for the inline query
        :param cache_time: The maximum amount of time in seconds that the result of the inline query
            may be cached on the server.
        :param is_personal: Pass True, if results may be cached on the server side only for
            the user that sent the query.
        :param next_offset: Pass the offset that a client should send in the next query with the same text
            to receive more results.
        :param switch_pm_parameter: If passed, clients will display a button with specified text that switches the user
            to a private chat with the bot and sends the bot a start message with the parameter switch_pm_parameter
        :param switch_pm_text:  Parameter for the start message sent to the bot when user presses the switch button
        :return: True means success.
        """
        return apihelper.answer_inline_query(self.token, inline_query_id, results, cache_time, is_personal, next_offset, switch_pm_text, switch_pm_parameter)

    def answer_callback_query(self, callback_query_id: str, text: Optional[str]=None, show_alert: Optional[bool]=None, url: Optional[str]=None, cache_time: Optional[int]=None) -> bool:
        """
        Use this method to send answers to callback queries sent from inline keyboards. The answer will be displayed to
        the user as a notification at the top of the chat screen or as an alert.
        :param callback_query_id:
        :param text:
        :param show_alert:
        :param url:
        :param cache_time:
        :return:
        """
        return apihelper.answer_callback_query(self.token, callback_query_id, text, show_alert, url, cache_time)

    def set_sticker_set_thumb(self, name: str, user_id: int, thumb: Union[(Any, str)]=None):
        """
        Use this method to set the thumbnail of a sticker set. 
        Animated thumbnails can be set for animated sticker sets only. Returns True on success.
        """
        return apihelper.set_sticker_set_thumb(self.token, name, user_id, thumb)

    def get_sticker_set(self, name: str) -> types.StickerSet:
        """
        Use this method to get a sticker set. On success, a StickerSet object is returned.
        :param name:
        :return:
        """
        result = apihelper.get_sticker_set(self.token, name)
        return types.StickerSet.de_json(result)

    def upload_sticker_file(self, user_id: int, png_sticker: Union[(Any, str)]) -> types.File:
        """
        Use this method to upload a .png file with a sticker for later use in createNewStickerSet and addStickerToSet
        methods (can be used multiple times). Returns the uploaded File on success.
        :param user_id:
        :param png_sticker:
        :return:
        """
        result = apihelper.upload_sticker_file(self.token, user_id, png_sticker)
        return types.File.de_json(result)

    def create_new_sticker_set(self, user_id: int, name: str, title: str, emojis: str, png_sticker: Union[(Any, str)], tgs_sticker: Union[(Any, str)], contains_masks: Optional[bool]=None, mask_position: Optional[types.MaskPosition]=None) -> bool:
        """
        Use this method to create new sticker set owned by a user. 
        The bot will be able to edit the created sticker set.
        Returns True on success.
        :param user_id:
        :param name:
        :param title:
        :param emojis:
        :param png_sticker: 
        :param tgs_sticker:
        :param contains_masks:
        :param mask_position:
        :return:
        """
        return apihelper.create_new_sticker_set(self.token, user_id, name, title, emojis, png_sticker, tgs_sticker, contains_masks, mask_position)

    def add_sticker_to_set(self, user_id: int, name: str, emojis: str, png_sticker: Optional[Union[(Any, str)]]=None, tgs_sticker: Optional[Union[(Any, str)]]=None, mask_position: Optional[types.MaskPosition]=None) -> bool:
        """
        Use this method to add a new sticker to a set created by the bot. 
        It's required to pass `png_sticker` or `tgs_sticker`.
        Returns True on success.
        :param user_id:
        :param name:
        :param emojis:
        :param png_sticker: Required if `tgs_sticker` is None
        :param tgs_sticker: Required if `png_sticker` is None
        :param mask_position:
        :return:
        """
        return apihelper.add_sticker_to_set(self.token, user_id, name, emojis, png_sticker, tgs_sticker, mask_position)

    def set_sticker_position_in_set(self, sticker: str, position: int) -> bool:
        """
        Use this method to move a sticker in a set created by the bot to a specific position . Returns True on success.
        :param sticker:
        :param position:
        :return:
        """
        return apihelper.set_sticker_position_in_set(self.token, sticker, position)

    def delete_sticker_from_set(self, sticker: str) -> bool:
        """
        Use this method to delete a sticker from a set created by the bot. Returns True on success.
        :param sticker:
        :return:
        """
        return apihelper.delete_sticker_from_set(self.token, sticker)

    def register_for_reply--- This code section failed: ---

 L.2281         0  LOAD_FAST                'message'
                2  LOAD_ATTR                message_id
                4  STORE_FAST               'message_id'

 L.2282         6  LOAD_FAST                'self'
                8  LOAD_ATTR                register_for_reply_by_message_id
               10  LOAD_FAST                'message_id'
               12  LOAD_FAST                'callback'
               14  BUILD_LIST_2          2 
               16  LOAD_FAST                'args'
               18  CALL_FINALLY         21  'to 21'
               20  WITH_CLEANUP_FINISH
               22  BUILD_MAP_0           0 
               24  LOAD_FAST                'kwargs'
               26  <164>                 1  ''
               28  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               30  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 18

    def register_for_reply_by_message_id--- This code section failed: ---

 L.2295         0  LOAD_FAST                'self'
                2  LOAD_ATTR                reply_backend
                4  LOAD_METHOD              register_handler
                6  LOAD_FAST                'message_id'
                8  LOAD_GLOBAL              Handler
               10  LOAD_FAST                'callback'
               12  BUILD_LIST_1          1 
               14  LOAD_FAST                'args'
               16  CALL_FINALLY         19  'to 19'
               18  WITH_CLEANUP_FINISH
               20  BUILD_MAP_0           0 
               22  LOAD_FAST                'kwargs'
               24  <164>                 1  ''
               26  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               28  CALL_METHOD_2         2  ''
               30  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def _notify_reply_handlers--- This code section failed: ---

 L.2303         0  LOAD_FAST                'new_messages'
                2  GET_ITER         
              4_0  COME_FROM            96  '96'
              4_1  COME_FROM            46  '46'
              4_2  COME_FROM            26  '26'
              4_3  COME_FROM            16  '16'
                4  FOR_ITER             98  'to 98'
                6  STORE_FAST               'message'

 L.2304         8  LOAD_GLOBAL              hasattr
               10  LOAD_FAST                'message'
               12  LOAD_STR                 'reply_to_message'
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_FALSE_BACK     4  'to 4'
               18  LOAD_FAST                'message'
               20  LOAD_ATTR                reply_to_message
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE_BACK     4  'to 4'

 L.2305        28  LOAD_FAST                'self'
               30  LOAD_ATTR                reply_backend
               32  LOAD_METHOD              get_handlers
               34  LOAD_FAST                'message'
               36  LOAD_ATTR                reply_to_message
               38  LOAD_ATTR                message_id
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'handlers'

 L.2306        44  LOAD_FAST                'handlers'
               46  POP_JUMP_IF_FALSE_BACK     4  'to 4'

 L.2307        48  LOAD_FAST                'handlers'
               50  GET_ITER         
             52_0  COME_FROM            94  '94'
               52  FOR_ITER             96  'to 96'
               54  STORE_FAST               'handler'

 L.2308        56  LOAD_FAST                'self'
               58  LOAD_ATTR                _exec_task
               60  LOAD_FAST                'handler'
               62  LOAD_STR                 'callback'
               64  BINARY_SUBSCR    
               66  LOAD_FAST                'message'
               68  BUILD_LIST_2          2 
               70  LOAD_FAST                'handler'
               72  LOAD_STR                 'args'
               74  BINARY_SUBSCR    
               76  CALL_FINALLY         79  'to 79'
               78  WITH_CLEANUP_FINISH
               80  BUILD_MAP_0           0 
               82  LOAD_FAST                'handler'
               84  LOAD_STR                 'kwargs'
               86  BINARY_SUBSCR    
               88  <164>                 1  ''
               90  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               92  POP_TOP          
               94  JUMP_BACK            52  'to 52'
             96_0  COME_FROM            52  '52'
               96  JUMP_BACK             4  'to 4'
             98_0  COME_FROM             4  '4'

Parse error at or near `<117>' instruction at offset 24

    def register_next_step_handler--- This code section failed: ---

 L.2322         0  LOAD_FAST                'message'
                2  LOAD_ATTR                chat
                4  LOAD_ATTR                id
                6  STORE_FAST               'chat_id'

 L.2323         8  LOAD_FAST                'self'
               10  LOAD_ATTR                register_next_step_handler_by_chat_id
               12  LOAD_FAST                'chat_id'
               14  LOAD_FAST                'callback'
               16  BUILD_LIST_2          2 
               18  LOAD_FAST                'args'
               20  CALL_FINALLY         23  'to 23'
               22  WITH_CLEANUP_FINISH
               24  BUILD_MAP_0           0 
               26  LOAD_FAST                'kwargs'
               28  <164>                 1  ''
               30  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               32  POP_TOP          

Parse error at or near `CALL_FINALLY' instruction at offset 20

    def register_next_step_handler_by_chat_id--- This code section failed: ---

 L.2337         0  LOAD_FAST                'self'
                2  LOAD_ATTR                next_step_backend
                4  LOAD_METHOD              register_handler
                6  LOAD_FAST                'chat_id'
                8  LOAD_GLOBAL              Handler
               10  LOAD_FAST                'callback'
               12  BUILD_LIST_1          1 
               14  LOAD_FAST                'args'
               16  CALL_FINALLY         19  'to 19'
               18  WITH_CLEANUP_FINISH
               20  BUILD_MAP_0           0 
               22  LOAD_FAST                'kwargs'
               24  <164>                 1  ''
               26  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               28  CALL_METHOD_2         2  ''
               30  POP_TOP          

Parse error at or near `None' instruction at offset -1

    def clear_step_handler(self, message: types.Message) -> None:
        """
        Clears all callback functions registered by register_next_step_handler().

        :param message:     The message for which we want to handle new message after that in same chat.
        """
        chat_id = message.chat.id
        self.clear_step_handler_by_chat_id(chat_id)

    def clear_step_handler_by_chat_id(self, chat_id: Union[(int, str)]) -> None:
        """
        Clears all callback functions registered by register_next_step_handler().

        :param chat_id: The chat for which we want to clear next step handlers
        """
        self.next_step_backend.clear_handlers(chat_id)

    def clear_reply_handlers(self, message: types.Message) -> None:
        """
        Clears all callback functions registered by register_for_reply() and register_for_reply_by_message_id().

        :param message: The message for which we want to clear reply handlers
        """
        message_id = message.message_id
        self.clear_reply_handlers_by_message_id(message_id)

    def clear_reply_handlers_by_message_id(self, message_id: int) -> None:
        """
        Clears all callback functions registered by register_for_reply() and register_for_reply_by_message_id().

        :param message_id: The message id for which we want to clear reply handlers
        """
        self.reply_backend.clear_handlers(message_id)

    def _notify_next_handlers--- This code section failed: ---

 L.2379         0  LOAD_GLOBAL              enumerate
                2  LOAD_FAST                'new_messages'
                4  CALL_FUNCTION_1       1  ''
                6  GET_ITER         
              8_0  COME_FROM           106  '106'
              8_1  COME_FROM            94  '94'
                8  FOR_ITER            108  'to 108'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'i'
               14  STORE_FAST               'message'

 L.2380        16  LOAD_CONST               False
               18  STORE_FAST               'need_pop'

 L.2381        20  LOAD_FAST                'self'
               22  LOAD_ATTR                next_step_backend
               24  LOAD_METHOD              get_handlers
               26  LOAD_FAST                'message'
               28  LOAD_ATTR                chat
               30  LOAD_ATTR                id
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'handlers'

 L.2382        36  LOAD_FAST                'handlers'
               38  POP_JUMP_IF_FALSE    92  'to 92'

 L.2383        40  LOAD_FAST                'handlers'
               42  GET_ITER         
             44_0  COME_FROM            90  '90'
               44  FOR_ITER             92  'to 92'
               46  STORE_FAST               'handler'

 L.2384        48  LOAD_CONST               True
               50  STORE_FAST               'need_pop'

 L.2385        52  LOAD_FAST                'self'
               54  LOAD_ATTR                _exec_task
               56  LOAD_FAST                'handler'
               58  LOAD_STR                 'callback'
               60  BINARY_SUBSCR    
               62  LOAD_FAST                'message'
               64  BUILD_LIST_2          2 
               66  LOAD_FAST                'handler'
               68  LOAD_STR                 'args'
               70  BINARY_SUBSCR    
               72  CALL_FINALLY         75  'to 75'
               74  WITH_CLEANUP_FINISH
               76  BUILD_MAP_0           0 
               78  LOAD_FAST                'handler'
               80  LOAD_STR                 'kwargs'
               82  BINARY_SUBSCR    
               84  <164>                 1  ''
               86  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               88  POP_TOP          
               90  JUMP_BACK            44  'to 44'
             92_0  COME_FROM            44  '44'
             92_1  COME_FROM            38  '38'

 L.2386        92  LOAD_FAST                'need_pop'
               94  POP_JUMP_IF_FALSE_BACK     8  'to 8'

 L.2387        96  LOAD_FAST                'new_messages'
               98  LOAD_METHOD              pop
              100  LOAD_FAST                'i'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          
              106  JUMP_BACK             8  'to 8'
            108_0  COME_FROM             8  '8'

Parse error at or near `CALL_FINALLY' instruction at offset 72

    @staticmethod
    def _build_handler_dict(handler, **filters):
        """
        Builds a dictionary for a handler
        :param handler:
        :param filters:
        :return:
        """
        return {'function':handler, 
         'filters':filters}

    def middleware_handler(self, update_types=None):
        """
        Middleware handler decorator.

        This decorator can be used to decorate functions that must be handled as middlewares before entering any other
        message handlers
        But, be careful and check type of the update inside the handler if more than one update_type is given

        Example:

        bot = TeleBot('TOKEN')

        # Print post message text before entering to any post_channel handlers
        @bot.middleware_handler(update_types=['channel_post', 'edited_channel_post'])
        def print_channel_post_text(bot_instance, channel_post):
            print(channel_post.text)

        # Print update id before entering to any handlers
        @bot.middleware_handler()
        def print_channel_post_text(bot_instance, update):
            print(update.update_id)

        :param update_types: Optional list of update types that can be passed into the middleware handler.

        """

        def decorator(handler):
            self.add_middleware_handler(handler, update_types)
            return handler

        return decorator

    def add_middleware_handler(self, handler, update_types=None):
        """
        Add middleware handler
        :param handler:
        :param update_types:
        :return:
        """
        if not apihelper.ENABLE_MIDDLEWARE:
            raise RuntimeError('Middleware is not enabled. Use apihelper.ENABLE_MIDDLEWARE.')
        if update_types:
            for update_type in update_types:
                self.typed_middleware_handlers[update_type].append(handler)

        else:
            self.default_middleware_handlers.append(handler)

    def message_handler--- This code section failed: ---

 L.2484         0  LOAD_DEREF               'content_types'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.2485         8  LOAD_STR                 'text'
               10  BUILD_LIST_1          1 
               12  STORE_DEREF              'content_types'
             14_0  COME_FROM             6  '6'

 L.2487        14  LOAD_CLOSURE             'commands'
               16  LOAD_CLOSURE             'content_types'
               18  LOAD_CLOSURE             'func'
               20  LOAD_CLOSURE             'kwargs'
               22  LOAD_CLOSURE             'regexp'
               24  LOAD_CLOSURE             'self'
               26  BUILD_TUPLE_6         6 
               28  LOAD_CODE                <code_object decorator>
               30  LOAD_STR                 'TeleBot.message_handler.<locals>.decorator'
               32  MAKE_FUNCTION_8          'closure'
               34  STORE_FAST               'decorator'

 L.2497        36  LOAD_FAST                'decorator'
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def add_message_handler(self, handler_dict):
        """
        Adds a message handler
        :param handler_dict:
        :return:
        """
        self.message_handlers.append(handler_dict)

    def edited_message_handler--- This code section failed: ---

 L.2518         0  LOAD_DEREF               'content_types'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.2519         8  LOAD_STR                 'text'
               10  BUILD_LIST_1          1 
               12  STORE_DEREF              'content_types'
             14_0  COME_FROM             6  '6'

 L.2521        14  LOAD_CLOSURE             'commands'
               16  LOAD_CLOSURE             'content_types'
               18  LOAD_CLOSURE             'func'
               20  LOAD_CLOSURE             'kwargs'
               22  LOAD_CLOSURE             'regexp'
               24  LOAD_CLOSURE             'self'
               26  BUILD_TUPLE_6         6 
               28  LOAD_CODE                <code_object decorator>
               30  LOAD_STR                 'TeleBot.edited_message_handler.<locals>.decorator'
               32  MAKE_FUNCTION_8          'closure'
               34  STORE_FAST               'decorator'

 L.2531        36  LOAD_FAST                'decorator'
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def add_edited_message_handler(self, handler_dict):
        """
        Adds the edit message handler
        :param handler_dict:
        :return:
        """
        self.edited_message_handlers.append(handler_dict)

    def channel_post_handler--- This code section failed: ---

 L.2552         0  LOAD_DEREF               'content_types'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.2553         8  LOAD_STR                 'text'
               10  BUILD_LIST_1          1 
               12  STORE_DEREF              'content_types'
             14_0  COME_FROM             6  '6'

 L.2555        14  LOAD_CLOSURE             'commands'
               16  LOAD_CLOSURE             'content_types'
               18  LOAD_CLOSURE             'func'
               20  LOAD_CLOSURE             'kwargs'
               22  LOAD_CLOSURE             'regexp'
               24  LOAD_CLOSURE             'self'
               26  BUILD_TUPLE_6         6 
               28  LOAD_CODE                <code_object decorator>
               30  LOAD_STR                 'TeleBot.channel_post_handler.<locals>.decorator'
               32  MAKE_FUNCTION_8          'closure'
               34  STORE_FAST               'decorator'

 L.2565        36  LOAD_FAST                'decorator'
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def add_channel_post_handler(self, handler_dict):
        """
        Adds channel post handler
        :param handler_dict:
        :return:
        """
        self.channel_post_handlers.append(handler_dict)

    def edited_channel_post_handler--- This code section failed: ---

 L.2586         0  LOAD_DEREF               'content_types'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.2587         8  LOAD_STR                 'text'
               10  BUILD_LIST_1          1 
               12  STORE_DEREF              'content_types'
             14_0  COME_FROM             6  '6'

 L.2589        14  LOAD_CLOSURE             'commands'
               16  LOAD_CLOSURE             'content_types'
               18  LOAD_CLOSURE             'func'
               20  LOAD_CLOSURE             'kwargs'
               22  LOAD_CLOSURE             'regexp'
               24  LOAD_CLOSURE             'self'
               26  BUILD_TUPLE_6         6 
               28  LOAD_CODE                <code_object decorator>
               30  LOAD_STR                 'TeleBot.edited_channel_post_handler.<locals>.decorator'
               32  MAKE_FUNCTION_8          'closure'
               34  STORE_FAST               'decorator'

 L.2599        36  LOAD_FAST                'decorator'
               38  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def add_edited_channel_post_handler(self, handler_dict):
        """
        Adds the edit channel post handler
        :param handler_dict:
        :return:
        """
        self.edited_channel_post_handlers.append(handler_dict)

    def inline_handler(self, func, **kwargs):
        """
        Inline call handler decorator
        :param func:
        :param kwargs:
        :return:
        """

        def decorator--- This code section failed: ---

 L.2618         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                _build_handler_dict
                4  LOAD_FAST                'handler'
                6  BUILD_TUPLE_1         1 
                8  LOAD_STR                 'func'
               10  LOAD_DEREF               'func'
               12  BUILD_MAP_1           1 
               14  LOAD_DEREF               'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  STORE_FAST               'handler_dict'

 L.2619        22  LOAD_DEREF               'self'
               24  LOAD_METHOD              add_inline_handler
               26  LOAD_FAST                'handler_dict'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.2620        32  LOAD_FAST                'handler'
               34  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

        return decorator

    def add_inline_handler(self, handler_dict):
        """
        Adds inline call handler
        :param handler_dict:
        :return:
        """
        self.inline_handlers.append(handler_dict)

    def chosen_inline_handler(self, func, **kwargs):
        """
        Description: TBD
        :param func:
        :param kwargs:
        :return:
        """

        def decorator--- This code section failed: ---

 L.2641         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                _build_handler_dict
                4  LOAD_FAST                'handler'
                6  BUILD_TUPLE_1         1 
                8  LOAD_STR                 'func'
               10  LOAD_DEREF               'func'
               12  BUILD_MAP_1           1 
               14  LOAD_DEREF               'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  STORE_FAST               'handler_dict'

 L.2642        22  LOAD_DEREF               'self'
               24  LOAD_METHOD              add_chosen_inline_handler
               26  LOAD_FAST                'handler_dict'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.2643        32  LOAD_FAST                'handler'
               34  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

        return decorator

    def add_chosen_inline_handler(self, handler_dict):
        """
        Description: TBD
        :param handler_dict:
        :return:
        """
        self.chosen_inline_handlers.append(handler_dict)

    def callback_query_handler(self, func, **kwargs):
        """
        Callback request handler decorator
        :param func:
        :param kwargs:
        :return:
        """

        def decorator--- This code section failed: ---

 L.2664         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                _build_handler_dict
                4  LOAD_FAST                'handler'
                6  BUILD_TUPLE_1         1 
                8  LOAD_STR                 'func'
               10  LOAD_DEREF               'func'
               12  BUILD_MAP_1           1 
               14  LOAD_DEREF               'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  STORE_FAST               'handler_dict'

 L.2665        22  LOAD_DEREF               'self'
               24  LOAD_METHOD              add_callback_query_handler
               26  LOAD_FAST                'handler_dict'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.2666        32  LOAD_FAST                'handler'
               34  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

        return decorator

    def add_callback_query_handler(self, handler_dict):
        """
        Adds a callback request handler
        :param handler_dict:
        :return:
        """
        self.callback_query_handlers.append(handler_dict)

    def shipping_query_handler(self, func, **kwargs):
        """
        Shipping request handler
        :param func:
        :param kwargs:
        :return:
        """

        def decorator--- This code section failed: ---

 L.2687         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                _build_handler_dict
                4  LOAD_FAST                'handler'
                6  BUILD_TUPLE_1         1 
                8  LOAD_STR                 'func'
               10  LOAD_DEREF               'func'
               12  BUILD_MAP_1           1 
               14  LOAD_DEREF               'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  STORE_FAST               'handler_dict'

 L.2688        22  LOAD_DEREF               'self'
               24  LOAD_METHOD              add_shipping_query_handler
               26  LOAD_FAST                'handler_dict'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.2689        32  LOAD_FAST                'handler'
               34  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

        return decorator

    def add_shipping_query_handler(self, handler_dict):
        """
        Adds a shipping request handler
        :param handler_dict:
        :return:
        """
        self.shipping_query_handlers.append(handler_dict)

    def pre_checkout_query_handler(self, func, **kwargs):
        """
        Pre-checkout request handler
        :param func:
        :param kwargs:
        :return:
        """

        def decorator--- This code section failed: ---

 L.2710         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                _build_handler_dict
                4  LOAD_FAST                'handler'
                6  BUILD_TUPLE_1         1 
                8  LOAD_STR                 'func'
               10  LOAD_DEREF               'func'
               12  BUILD_MAP_1           1 
               14  LOAD_DEREF               'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  STORE_FAST               'handler_dict'

 L.2711        22  LOAD_DEREF               'self'
               24  LOAD_METHOD              add_pre_checkout_query_handler
               26  LOAD_FAST                'handler_dict'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.2712        32  LOAD_FAST                'handler'
               34  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

        return decorator

    def add_pre_checkout_query_handler(self, handler_dict):
        """
        Adds a pre-checkout request handler
        :param handler_dict:
        :return:
        """
        self.pre_checkout_query_handlers.append(handler_dict)

    def poll_handler(self, func, **kwargs):
        """
        Poll request handler
        :param func:
        :param kwargs:
        :return:
        """

        def decorator--- This code section failed: ---

 L.2733         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                _build_handler_dict
                4  LOAD_FAST                'handler'
                6  BUILD_TUPLE_1         1 
                8  LOAD_STR                 'func'
               10  LOAD_DEREF               'func'
               12  BUILD_MAP_1           1 
               14  LOAD_DEREF               'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  STORE_FAST               'handler_dict'

 L.2734        22  LOAD_DEREF               'self'
               24  LOAD_METHOD              add_poll_handler
               26  LOAD_FAST                'handler_dict'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.2735        32  LOAD_FAST                'handler'
               34  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

        return decorator

    def add_poll_handler(self, handler_dict):
        """
        Adds a poll request handler
        :param handler_dict:
        :return:
        """
        self.poll_handlers.append(handler_dict)

    def poll_answer_handler(self, func=None, **kwargs):
        """
        Poll_answer request handler
        :param func:
        :param kwargs:
        :return:
        """

        def decorator--- This code section failed: ---

 L.2756         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                _build_handler_dict
                4  LOAD_FAST                'handler'
                6  BUILD_TUPLE_1         1 
                8  LOAD_STR                 'func'
               10  LOAD_DEREF               'func'
               12  BUILD_MAP_1           1 
               14  LOAD_DEREF               'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  STORE_FAST               'handler_dict'

 L.2757        22  LOAD_DEREF               'self'
               24  LOAD_METHOD              add_poll_answer_handler
               26  LOAD_FAST                'handler_dict'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.2758        32  LOAD_FAST                'handler'
               34  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

        return decorator

    def add_poll_answer_handler(self, handler_dict):
        """
        Adds a poll_answer request handler
        :param handler_dict:
        :return:
        """
        self.poll_answer_handlers.append(handler_dict)

    def my_chat_member_handler(self, func=None, **kwargs):
        """
        my_chat_member handler
        :param func:
        :param kwargs:
        :return:
        """

        def decorator--- This code section failed: ---

 L.2779         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                _build_handler_dict
                4  LOAD_FAST                'handler'
                6  BUILD_TUPLE_1         1 
                8  LOAD_STR                 'func'
               10  LOAD_DEREF               'func'
               12  BUILD_MAP_1           1 
               14  LOAD_DEREF               'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  STORE_FAST               'handler_dict'

 L.2780        22  LOAD_DEREF               'self'
               24  LOAD_METHOD              add_my_chat_member_handler
               26  LOAD_FAST                'handler_dict'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.2781        32  LOAD_FAST                'handler'
               34  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

        return decorator

    def add_my_chat_member_handler(self, handler_dict):
        """
        Adds a my_chat_member handler
        :param handler_dict:
        :return:
        """
        self.my_chat_member_handlers.append(handler_dict)

    def chat_member_handler(self, func=None, **kwargs):
        """
        chat_member handler
        :param func:
        :param kwargs:
        :return:
        """

        def decorator--- This code section failed: ---

 L.2802         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                _build_handler_dict
                4  LOAD_FAST                'handler'
                6  BUILD_TUPLE_1         1 
                8  LOAD_STR                 'func'
               10  LOAD_DEREF               'func'
               12  BUILD_MAP_1           1 
               14  LOAD_DEREF               'kwargs'
               16  <164>                 1  ''
               18  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               20  STORE_FAST               'handler_dict'

 L.2803        22  LOAD_DEREF               'self'
               24  LOAD_METHOD              add_chat_member_handler
               26  LOAD_FAST                'handler_dict'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.2804        32  LOAD_FAST                'handler'
               34  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

        return decorator

    def add_chat_member_handler(self, handler_dict):
        """
        Adds a chat_member handler
        :param handler_dict:
        :return:
        """
        self.chat_member_handlers.append(handler_dict)

    def _test_message_handler--- This code section failed: ---

 L.2824         0  LOAD_FAST                'message_handler'
                2  LOAD_STR                 'filters'
                4  BINARY_SUBSCR    
                6  LOAD_METHOD              items
                8  CALL_METHOD_0         0  ''
               10  GET_ITER         
             12_0  COME_FROM            50  '50'
             12_1  COME_FROM            42  '42'
             12_2  COME_FROM            28  '28'
               12  FOR_ITER             52  'to 52'
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'message_filter'
               18  STORE_FAST               'filter_value'

 L.2825        20  LOAD_FAST                'filter_value'
               22  LOAD_CONST               None
               24  <117>                 0  ''
               26  POP_JUMP_IF_FALSE    30  'to 30'

 L.2826        28  JUMP_BACK            12  'to 12'
             30_0  COME_FROM            26  '26'

 L.2828        30  LOAD_FAST                'self'
               32  LOAD_METHOD              _test_filter
               34  LOAD_FAST                'message_filter'
               36  LOAD_FAST                'filter_value'
               38  LOAD_FAST                'message'
               40  CALL_METHOD_3         3  ''
               42  POP_JUMP_IF_TRUE_BACK    12  'to 12'

 L.2829        44  POP_TOP          
               46  LOAD_CONST               False
               48  RETURN_VALUE     
               50  JUMP_BACK            12  'to 12'
             52_0  COME_FROM            12  '12'

 L.2831        52  LOAD_CONST               True
               54  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `<117>' instruction at offset 24

    @staticmethod
    def _test_filter(message_filter, filter_value, message):
        """
        Test filters
        :param message_filter:
        :param filter_value:
        :param message:
        :return:
        """
        test_cases = {'content_types':--- This code section failed: ---

 L.2843         0  LOAD_FAST                'msg'
                2  LOAD_ATTR                content_type
                4  LOAD_DEREF               'filter_value'
                6  <118>                 0  ''
                8  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
,  'regexp':lambda msg: msg.content_type == 'text' and re.search(filter_value, msg.text, re.IGNORECASE), 
         'commands':--- This code section failed: ---

 L.2845         0  LOAD_FAST                'msg'
                2  LOAD_ATTR                content_type
                4  LOAD_STR                 'text'
                6  COMPARE_OP               ==
                8  JUMP_IF_FALSE_OR_POP    24  'to 24'
               10  LOAD_GLOBAL              util
               12  LOAD_METHOD              extract_command
               14  LOAD_FAST                'msg'
               16  LOAD_ATTR                text
               18  CALL_METHOD_1         1  ''
               20  LOAD_DEREF               'filter_value'
               22  <118>                 0  ''
             24_0  COME_FROM             8  '8'
               24  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
,  'func':lambda msg: filter_value(msg)}
        return test_cases.get(message_filter, lambda msg: False)(message)

    def _notify_command_handlers(self, handlers, new_messages):
        """
        Notifies command handlers
        :param handlers:
        :param new_messages:
        :return:
        """
        if len(handlers) == 0:
            return
        for message in new_messages:
            for message_handler in handlers:
                if self._test_message_handler(message_handler, message):
                    self._exec_task(message_handler['function'], message)
                    break


class AsyncTeleBot(TeleBot):

    def __init__--- This code section failed: ---

 L.2869         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                __init__
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  POP_TOP          

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def enable_save_next_step_handlers(self, delay=120, filename='./.handler-saves/step.save'):
        return TeleBot.enable_save_next_step_handlers(self, delay, filename)

    @util.async_dec()
    def enable_save_reply_handlers(self, delay=120, filename='./.handler-saves/reply.save'):
        return TeleBot.enable_save_reply_handlers(self, delay, filename)

    @util.async_dec()
    def disable_save_next_step_handlers(self):
        return TeleBot.disable_save_next_step_handlers(self)

    @util.async_dec()
    def disable_save_reply_handlers(self):
        return TeleBot.enable_save_reply_handlers(self)

    @util.async_dec()
    def load_next_step_handlers(self, filename='./.handler-saves/step.save', del_file_after_loading=True):
        return TeleBot.load_next_step_handlers(self, filename, del_file_after_loading)

    @util.async_dec()
    def load_reply_handlers(self, filename='./.handler-saves/reply.save', del_file_after_loading=True):
        return TeleBot.load_reply_handlers(self, filename, del_file_after_loading)

    @util.async_dec()
    def get_me(self):
        return TeleBot.get_me(self)

    @util.async_dec()
    def log_out(self):
        return TeleBot.log_out(self)

    @util.async_dec()
    def close(self):
        return TeleBot.close(self)

    @util.async_dec()
    def get_my_commands(self):
        return TeleBot.get_my_commands(self)

    @util.async_dec()
    def set_my_commands--- This code section failed: ---

 L.2915         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                set_my_commands
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def get_file--- This code section failed: ---

 L.2919         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                get_file
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def download_file--- This code section failed: ---

 L.2923         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                download_file
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def get_user_profile_photos--- This code section failed: ---

 L.2927         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                get_user_profile_photos
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def get_chat--- This code section failed: ---

 L.2931         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                get_chat
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def leave_chat--- This code section failed: ---

 L.2935         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                leave_chat
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def get_chat_administrators--- This code section failed: ---

 L.2939         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                get_chat_administrators
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def get_chat_members_count--- This code section failed: ---

 L.2943         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                get_chat_members_count
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def set_chat_sticker_set--- This code section failed: ---

 L.2947         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                set_chat_sticker_set
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def delete_chat_sticker_set--- This code section failed: ---

 L.2951         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                delete_chat_sticker_set
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def get_chat_member--- This code section failed: ---

 L.2955         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                get_chat_member
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_message--- This code section failed: ---

 L.2959         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_message
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_dice--- This code section failed: ---

 L.2963         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_dice
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_animation--- This code section failed: ---

 L.2967         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_animation
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def forward_message--- This code section failed: ---

 L.2971         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                forward_message
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def copy_message--- This code section failed: ---

 L.2975         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                copy_message
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def delete_message--- This code section failed: ---

 L.2979         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                delete_message
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_photo--- This code section failed: ---

 L.2983         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_photo
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_audio--- This code section failed: ---

 L.2987         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_audio
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_voice--- This code section failed: ---

 L.2991         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_voice
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_document--- This code section failed: ---

 L.2995         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_document
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_sticker--- This code section failed: ---

 L.2999         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_sticker
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_video--- This code section failed: ---

 L.3003         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_video
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_video_note--- This code section failed: ---

 L.3007         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_video_note
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_media_group--- This code section failed: ---

 L.3011         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_media_group
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_location--- This code section failed: ---

 L.3015         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_location
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def edit_message_live_location--- This code section failed: ---

 L.3019         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                edit_message_live_location
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def stop_message_live_location--- This code section failed: ---

 L.3023         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                stop_message_live_location
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_venue--- This code section failed: ---

 L.3027         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_venue
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_contact--- This code section failed: ---

 L.3031         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_contact
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_chat_action--- This code section failed: ---

 L.3035         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_chat_action
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def kick_chat_member--- This code section failed: ---

 L.3039         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                kick_chat_member
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def unban_chat_member--- This code section failed: ---

 L.3043         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                unban_chat_member
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def restrict_chat_member--- This code section failed: ---

 L.3047         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                restrict_chat_member
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def promote_chat_member--- This code section failed: ---

 L.3051         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                promote_chat_member
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def set_chat_administrator_custom_title--- This code section failed: ---

 L.3055         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                set_chat_administrator_custom_title
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def set_chat_permissions--- This code section failed: ---

 L.3059         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                set_chat_permissions
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def create_chat_invite_link--- This code section failed: ---

 L.3063         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                create_chat_invite_link
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def edit_chat_invite_link--- This code section failed: ---

 L.3067         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                edit_chat_invite_link
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def revoke_chat_invite_link--- This code section failed: ---

 L.3071         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                revoke_chat_invite_link
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def export_chat_invite_link--- This code section failed: ---

 L.3075         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                export_chat_invite_link
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def set_chat_photo--- This code section failed: ---

 L.3079         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                set_chat_photo
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def delete_chat_photo--- This code section failed: ---

 L.3083         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                delete_chat_photo
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def set_chat_title--- This code section failed: ---

 L.3087         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                set_chat_title
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def set_chat_description--- This code section failed: ---

 L.3091         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                set_chat_description
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def pin_chat_message--- This code section failed: ---

 L.3095         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                pin_chat_message
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def unpin_chat_message--- This code section failed: ---

 L.3099         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                unpin_chat_message
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def unpin_all_chat_messages--- This code section failed: ---

 L.3103         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                unpin_all_chat_messages
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  CALL_FUNCTION_EX      0  'positional arguments only'
               16  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def edit_message_text--- This code section failed: ---

 L.3107         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                edit_message_text
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def edit_message_media--- This code section failed: ---

 L.3111         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                edit_message_media
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def edit_message_reply_markup--- This code section failed: ---

 L.3115         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                edit_message_reply_markup
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_game--- This code section failed: ---

 L.3119         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_game
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def set_game_score--- This code section failed: ---

 L.3123         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                set_game_score
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def get_game_high_scores--- This code section failed: ---

 L.3127         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                get_game_high_scores
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_invoice--- This code section failed: ---

 L.3131         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_invoice
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def answer_shipping_query--- This code section failed: ---

 L.3135         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                answer_shipping_query
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def answer_pre_checkout_query--- This code section failed: ---

 L.3139         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                answer_pre_checkout_query
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def edit_message_caption--- This code section failed: ---

 L.3143         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                edit_message_caption
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def answer_inline_query--- This code section failed: ---

 L.3147         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                answer_inline_query
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def answer_callback_query--- This code section failed: ---

 L.3151         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                answer_callback_query
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def get_sticker_set--- This code section failed: ---

 L.3155         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                get_sticker_set
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def upload_sticker_file--- This code section failed: ---

 L.3159         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                upload_sticker_file
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def create_new_sticker_set--- This code section failed: ---

 L.3163         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                create_new_sticker_set
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def add_sticker_to_set--- This code section failed: ---

 L.3167         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                add_sticker_to_set
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def set_sticker_position_in_set--- This code section failed: ---

 L.3171         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                set_sticker_position_in_set
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def delete_sticker_from_set--- This code section failed: ---

 L.3175         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                delete_sticker_from_set
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def set_sticker_set_thumb--- This code section failed: ---

 L.3179         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                set_sticker_set_thumb
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def send_poll--- This code section failed: ---

 L.3183         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                send_poll
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    @util.async_dec()
    def stop_poll--- This code section failed: ---

 L.3187         0  LOAD_GLOBAL              TeleBot
                2  LOAD_ATTR                stop_poll
                4  LOAD_FAST                'self'
                6  BUILD_LIST_1          1 
                8  LOAD_FAST                'args'
               10  CALL_FINALLY         13  'to 13'
               12  WITH_CLEANUP_FINISH
               14  BUILD_MAP_0           0 
               16  LOAD_FAST                'kwargs'
               18  <164>                 1  ''
               20  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               22  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1