# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: telebot\__init__.py
from __future__ import print_function
import logging, re, sys, threading, time, traceback
logger = logging.getLogger('TeleBot')
formatter = logging.Formatter('%(asctime)s (%(filename)s:%(lineno)d %(threadName)s) %(levelname)s - %(name)s: "%(message)s"')
console_output_handler = logging.StreamHandler(sys.stderr)
console_output_handler.setFormatter(formatter)
logger.addHandler(console_output_handler)
logger.setLevel(logging.ERROR)
from telebot import apihelper, types, util
from telebot.handler_backends import MemoryHandlerBackend, FileHandlerBackend

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
    __doc__ = ' This is TeleBot Class\n    Methods:\n        getMe\n        sendMessage\n        forwardMessage\n        deleteMessage\n        sendPhoto\n        sendAudio\n        sendDocument\n        sendSticker\n        sendVideo\n        sendAnimation\n        sendVideoNote\n        sendLocation\n        sendChatAction\n        sendDice\n        getUserProfilePhotos\n        getUpdates\n        getFile\n        sendPoll\n        kickChatMember\n        unbanChatMember\n        restrictChatMember\n        promoteChatMember\n        exportChatInviteLink\n        setChatPhoto\n        deleteChatPhoto\n        setChatTitle\n        setChatDescription\n        pinChatMessage\n        unpinChatMessage\n        leaveChat\n        getChat\n        getChatAdministrators\n        getChatMembersCount\n        getChatMember\n        answerCallbackQuery\n        setMyCommands\n        answerInlineQuery\n        '

    def __init__(self, token, parse_mode=None, threaded=True, skip_pending=False, num_threads=2, next_step_backend=None, reply_backend=None, exception_handler=None, last_update_id=0):
        """
        :param token: bot API token
        :param parse_mode: default parse_mode
        :return: Telebot object.
        """
        self.token = token
        self.parse_mode = parse_mode
        self.update_listener = []
        self.skip_pending = skip_pending
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
        if apihelper.ENABLE_MIDDLEWARE:
            self.typed_middleware_handlers = {'message':[],  'edited_message':[],  'channel_post':[],  'edited_channel_post':[],  'inline_query':[],  'chosen_inline_result':[],  'callback_query':[],  'shipping_query':[],  'pre_checkout_query':[],  'poll':[]}
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
        update for the bot, we will send an HTTPS POST request to the specified url, containing a JSON-serialized Update.
        In case of an unsuccessful request, we will give up after a reasonable amount of attempts. Returns True on success.

        :param url: HTTPS url to send updates to. Use an empty string to remove webhook integration
        :param certificate: Upload your public key certificate so that the root certificate in use can be checked. See our self-signed guide for details.
        :param max_connections: Maximum allowed number of simultaneous HTTPS connections to the webhook for update delivery, 1-100. Defaults to 40. Use lower values to limit the load on your bot's server, and higher values to increase your bot's throughput.
        :param allowed_updates: A JSON-serialized list of the update types you want your bot to receive. For example, specify [“message”, “edited_channel_post”, “callback_query”] to only receive updates of these types. See Update for a complete list of available update types. Specify an empty list to receive all updates regardless of type (default). If not specified, the previous setting will be used.
        :param ip_address: The fixed IP address which will be used to send webhook requests instead of the IP address resolved through DNS
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

    def get_updates(self, offset=None, limit=None, timeout=20, allowed_updates=None, long_polling_timeout=20):
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
        while updates:
            total += len(updates)
            for update in updates:
                if update.update_id > self.last_update_id:
                    self.last_update_id = update.update_id
                updates = self.get_updates(offset=(self.last_update_id + 1), long_polling_timeout=1)

        return total

    def __retrieve_updates(self, timeout=20, long_polling_timeout=20):
        """
        Retrieves any updates from the Telegram API.
        Registered listeners and applicable message handlers will be notified when a new message arrives.
        :raises ApiException when a call has failed.
        """
        if self.skip_pending:
            logger.debug('Skipped {0} pending messages'.format(self._TeleBot__skip_updates()))
            self.skip_pending = False
        updates = self.get_updates(offset=(self.last_update_id + 1), timeout=timeout, long_polling_timeout=long_polling_timeout)
        self.process_new_updates(updates)

    def process_new_updates--- This code section failed: ---

 L. 326         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'updates'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'upd_count'

 L. 327         8  LOAD_GLOBAL              logger
               10  LOAD_METHOD              debug
               12  LOAD_STR                 'Received {0} new updates'
               14  LOAD_METHOD              format
               16  LOAD_FAST                'upd_count'
               18  CALL_METHOD_1         1  ''
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          

 L. 328        24  LOAD_FAST                'upd_count'
               26  LOAD_CONST               0
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    36  'to 36'

 L. 329        32  LOAD_CONST               None
               34  RETURN_VALUE     
             36_0  COME_FROM            30  '30'

 L. 331        36  LOAD_CONST               None
               38  STORE_FAST               'new_messages'

 L. 332        40  LOAD_CONST               None
               42  STORE_FAST               'new_edited_messages'

 L. 333        44  LOAD_CONST               None
               46  STORE_FAST               'new_channel_posts'

 L. 334        48  LOAD_CONST               None
               50  STORE_FAST               'new_edited_channel_posts'

 L. 335        52  LOAD_CONST               None
               54  STORE_FAST               'new_inline_queries'

 L. 336        56  LOAD_CONST               None
               58  STORE_FAST               'new_chosen_inline_results'

 L. 337        60  LOAD_CONST               None
               62  STORE_FAST               'new_callback_queries'

 L. 338        64  LOAD_CONST               None
               66  STORE_FAST               'new_shipping_queries'

 L. 339        68  LOAD_CONST               None
               70  STORE_FAST               'new_pre_checkout_queries'

 L. 340        72  LOAD_CONST               None
               74  STORE_FAST               'new_polls'

 L. 341        76  LOAD_CONST               None
               78  STORE_FAST               'new_poll_answers'

 L. 343        80  LOAD_FAST                'updates'
               82  GET_ITER         
             84_0  COME_FROM           454  '454'
            84_86  FOR_ITER            484  'to 484'
               88  STORE_FAST               'update'

 L. 344        90  LOAD_GLOBAL              apihelper
               92  LOAD_ATTR                ENABLE_MIDDLEWARE
               94  POP_JUMP_IF_FALSE   106  'to 106'

 L. 345        96  LOAD_FAST                'self'
               98  LOAD_METHOD              process_middlewares
              100  LOAD_FAST                'update'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          
            106_0  COME_FROM            94  '94'

 L. 347       106  LOAD_FAST                'update'
              108  LOAD_ATTR                update_id
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                last_update_id
              114  COMPARE_OP               >
              116  POP_JUMP_IF_FALSE   126  'to 126'

 L. 348       118  LOAD_FAST                'update'
              120  LOAD_ATTR                update_id
              122  LOAD_FAST                'self'
              124  STORE_ATTR               last_update_id
            126_0  COME_FROM           116  '116'

 L. 349       126  LOAD_FAST                'update'
              128  LOAD_ATTR                message
              130  POP_JUMP_IF_FALSE   156  'to 156'

 L. 350       132  LOAD_FAST                'new_messages'
              134  LOAD_CONST               None
              136  <117>                 0  ''
              138  POP_JUMP_IF_FALSE   144  'to 144'
              140  BUILD_LIST_0          0 
              142  STORE_FAST               'new_messages'
            144_0  COME_FROM           138  '138'

 L. 351       144  LOAD_FAST                'new_messages'
              146  LOAD_METHOD              append
              148  LOAD_FAST                'update'
              150  LOAD_ATTR                message
              152  CALL_METHOD_1         1  ''
              154  POP_TOP          
            156_0  COME_FROM           130  '130'

 L. 352       156  LOAD_FAST                'update'
              158  LOAD_ATTR                edited_message
              160  POP_JUMP_IF_FALSE   186  'to 186'

 L. 353       162  LOAD_FAST                'new_edited_messages'
              164  LOAD_CONST               None
              166  <117>                 0  ''
              168  POP_JUMP_IF_FALSE   174  'to 174'
              170  BUILD_LIST_0          0 
              172  STORE_FAST               'new_edited_messages'
            174_0  COME_FROM           168  '168'

 L. 354       174  LOAD_FAST                'new_edited_messages'
              176  LOAD_METHOD              append
              178  LOAD_FAST                'update'
              180  LOAD_ATTR                edited_message
              182  CALL_METHOD_1         1  ''
              184  POP_TOP          
            186_0  COME_FROM           160  '160'

 L. 355       186  LOAD_FAST                'update'
              188  LOAD_ATTR                channel_post
              190  POP_JUMP_IF_FALSE   216  'to 216'

 L. 356       192  LOAD_FAST                'new_channel_posts'
              194  LOAD_CONST               None
              196  <117>                 0  ''
              198  POP_JUMP_IF_FALSE   204  'to 204'
              200  BUILD_LIST_0          0 
              202  STORE_FAST               'new_channel_posts'
            204_0  COME_FROM           198  '198'

 L. 357       204  LOAD_FAST                'new_channel_posts'
              206  LOAD_METHOD              append
              208  LOAD_FAST                'update'
              210  LOAD_ATTR                channel_post
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          
            216_0  COME_FROM           190  '190'

 L. 358       216  LOAD_FAST                'update'
              218  LOAD_ATTR                edited_channel_post
              220  POP_JUMP_IF_FALSE   246  'to 246'

 L. 359       222  LOAD_FAST                'new_edited_channel_posts'
              224  LOAD_CONST               None
              226  <117>                 0  ''
              228  POP_JUMP_IF_FALSE   234  'to 234'
              230  BUILD_LIST_0          0 
              232  STORE_FAST               'new_edited_channel_posts'
            234_0  COME_FROM           228  '228'

 L. 360       234  LOAD_FAST                'new_edited_channel_posts'
              236  LOAD_METHOD              append
              238  LOAD_FAST                'update'
              240  LOAD_ATTR                edited_channel_post
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          
            246_0  COME_FROM           220  '220'

 L. 361       246  LOAD_FAST                'update'
              248  LOAD_ATTR                inline_query
          250_252  POP_JUMP_IF_FALSE   280  'to 280'

 L. 362       254  LOAD_FAST                'new_inline_queries'
              256  LOAD_CONST               None
              258  <117>                 0  ''
          260_262  POP_JUMP_IF_FALSE   268  'to 268'
              264  BUILD_LIST_0          0 
              266  STORE_FAST               'new_inline_queries'
            268_0  COME_FROM           260  '260'

 L. 363       268  LOAD_FAST                'new_inline_queries'
              270  LOAD_METHOD              append
              272  LOAD_FAST                'update'
              274  LOAD_ATTR                inline_query
              276  CALL_METHOD_1         1  ''
              278  POP_TOP          
            280_0  COME_FROM           250  '250'

 L. 364       280  LOAD_FAST                'update'
              282  LOAD_ATTR                chosen_inline_result
          284_286  POP_JUMP_IF_FALSE   314  'to 314'

 L. 365       288  LOAD_FAST                'new_chosen_inline_results'
              290  LOAD_CONST               None
              292  <117>                 0  ''
          294_296  POP_JUMP_IF_FALSE   302  'to 302'
              298  BUILD_LIST_0          0 
              300  STORE_FAST               'new_chosen_inline_results'
            302_0  COME_FROM           294  '294'

 L. 366       302  LOAD_FAST                'new_chosen_inline_results'
              304  LOAD_METHOD              append
              306  LOAD_FAST                'update'
              308  LOAD_ATTR                chosen_inline_result
              310  CALL_METHOD_1         1  ''
              312  POP_TOP          
            314_0  COME_FROM           284  '284'

 L. 367       314  LOAD_FAST                'update'
              316  LOAD_ATTR                callback_query
          318_320  POP_JUMP_IF_FALSE   348  'to 348'

 L. 368       322  LOAD_FAST                'new_callback_queries'
              324  LOAD_CONST               None
              326  <117>                 0  ''
          328_330  POP_JUMP_IF_FALSE   336  'to 336'
              332  BUILD_LIST_0          0 
              334  STORE_FAST               'new_callback_queries'
            336_0  COME_FROM           328  '328'

 L. 369       336  LOAD_FAST                'new_callback_queries'
              338  LOAD_METHOD              append
              340  LOAD_FAST                'update'
              342  LOAD_ATTR                callback_query
              344  CALL_METHOD_1         1  ''
              346  POP_TOP          
            348_0  COME_FROM           318  '318'

 L. 370       348  LOAD_FAST                'update'
              350  LOAD_ATTR                shipping_query
          352_354  POP_JUMP_IF_FALSE   382  'to 382'

 L. 371       356  LOAD_FAST                'new_shipping_queries'
              358  LOAD_CONST               None
              360  <117>                 0  ''
          362_364  POP_JUMP_IF_FALSE   370  'to 370'
              366  BUILD_LIST_0          0 
              368  STORE_FAST               'new_shipping_queries'
            370_0  COME_FROM           362  '362'

 L. 372       370  LOAD_FAST                'new_shipping_queries'
              372  LOAD_METHOD              append
              374  LOAD_FAST                'update'
              376  LOAD_ATTR                shipping_query
              378  CALL_METHOD_1         1  ''
              380  POP_TOP          
            382_0  COME_FROM           352  '352'

 L. 373       382  LOAD_FAST                'update'
              384  LOAD_ATTR                pre_checkout_query
          386_388  POP_JUMP_IF_FALSE   416  'to 416'

 L. 374       390  LOAD_FAST                'new_pre_checkout_queries'
              392  LOAD_CONST               None
              394  <117>                 0  ''
          396_398  POP_JUMP_IF_FALSE   404  'to 404'
              400  BUILD_LIST_0          0 
              402  STORE_FAST               'new_pre_checkout_queries'
            404_0  COME_FROM           396  '396'

 L. 375       404  LOAD_FAST                'new_pre_checkout_queries'
              406  LOAD_METHOD              append
              408  LOAD_FAST                'update'
              410  LOAD_ATTR                pre_checkout_query
              412  CALL_METHOD_1         1  ''
              414  POP_TOP          
            416_0  COME_FROM           386  '386'

 L. 376       416  LOAD_FAST                'update'
              418  LOAD_ATTR                poll
          420_422  POP_JUMP_IF_FALSE   450  'to 450'

 L. 377       424  LOAD_FAST                'new_polls'
              426  LOAD_CONST               None
              428  <117>                 0  ''
          430_432  POP_JUMP_IF_FALSE   438  'to 438'
              434  BUILD_LIST_0          0 
              436  STORE_FAST               'new_polls'
            438_0  COME_FROM           430  '430'

 L. 378       438  LOAD_FAST                'new_polls'
              440  LOAD_METHOD              append
              442  LOAD_FAST                'update'
              444  LOAD_ATTR                poll
              446  CALL_METHOD_1         1  ''
              448  POP_TOP          
            450_0  COME_FROM           420  '420'

 L. 379       450  LOAD_FAST                'update'
              452  LOAD_ATTR                poll_answer
              454  POP_JUMP_IF_FALSE    84  'to 84'

 L. 380       456  LOAD_FAST                'new_poll_answers'
              458  LOAD_CONST               None
              460  <117>                 0  ''
          462_464  POP_JUMP_IF_FALSE   470  'to 470'
              466  BUILD_LIST_0          0 
              468  STORE_FAST               'new_poll_answers'
            470_0  COME_FROM           462  '462'

 L. 381       470  LOAD_FAST                'new_poll_answers'
              472  LOAD_METHOD              append
              474  LOAD_FAST                'update'
              476  LOAD_ATTR                poll_answer
              478  CALL_METHOD_1         1  ''
              480  POP_TOP          
              482  JUMP_BACK            84  'to 84'

 L. 383       484  LOAD_FAST                'new_messages'
          486_488  POP_JUMP_IF_FALSE   500  'to 500'

 L. 384       490  LOAD_FAST                'self'
              492  LOAD_METHOD              process_new_messages
              494  LOAD_FAST                'new_messages'
              496  CALL_METHOD_1         1  ''
              498  POP_TOP          
            500_0  COME_FROM           486  '486'

 L. 385       500  LOAD_FAST                'new_edited_messages'
          502_504  POP_JUMP_IF_FALSE   516  'to 516'

 L. 386       506  LOAD_FAST                'self'
              508  LOAD_METHOD              process_new_edited_messages
              510  LOAD_FAST                'new_edited_messages'
              512  CALL_METHOD_1         1  ''
              514  POP_TOP          
            516_0  COME_FROM           502  '502'

 L. 387       516  LOAD_FAST                'new_channel_posts'
          518_520  POP_JUMP_IF_FALSE   532  'to 532'

 L. 388       522  LOAD_FAST                'self'
              524  LOAD_METHOD              process_new_channel_posts
              526  LOAD_FAST                'new_channel_posts'
              528  CALL_METHOD_1         1  ''
              530  POP_TOP          
            532_0  COME_FROM           518  '518'

 L. 389       532  LOAD_FAST                'new_edited_channel_posts'
          534_536  POP_JUMP_IF_FALSE   548  'to 548'

 L. 390       538  LOAD_FAST                'self'
              540  LOAD_METHOD              process_new_edited_channel_posts
              542  LOAD_FAST                'new_edited_channel_posts'
              544  CALL_METHOD_1         1  ''
              546  POP_TOP          
            548_0  COME_FROM           534  '534'

 L. 391       548  LOAD_FAST                'new_inline_queries'
          550_552  POP_JUMP_IF_FALSE   564  'to 564'

 L. 392       554  LOAD_FAST                'self'
              556  LOAD_METHOD              process_new_inline_query
              558  LOAD_FAST                'new_inline_queries'
              560  CALL_METHOD_1         1  ''
              562  POP_TOP          
            564_0  COME_FROM           550  '550'

 L. 393       564  LOAD_FAST                'new_chosen_inline_results'
          566_568  POP_JUMP_IF_FALSE   580  'to 580'

 L. 394       570  LOAD_FAST                'self'
              572  LOAD_METHOD              process_new_chosen_inline_query
              574  LOAD_FAST                'new_chosen_inline_results'
              576  CALL_METHOD_1         1  ''
              578  POP_TOP          
            580_0  COME_FROM           566  '566'

 L. 395       580  LOAD_FAST                'new_callback_queries'
          582_584  POP_JUMP_IF_FALSE   596  'to 596'

 L. 396       586  LOAD_FAST                'self'
              588  LOAD_METHOD              process_new_callback_query
              590  LOAD_FAST                'new_callback_queries'
              592  CALL_METHOD_1         1  ''
              594  POP_TOP          
            596_0  COME_FROM           582  '582'

 L. 397       596  LOAD_FAST                'new_shipping_queries'
          598_600  POP_JUMP_IF_FALSE   612  'to 612'

 L. 398       602  LOAD_FAST                'self'
              604  LOAD_METHOD              process_new_shipping_query
              606  LOAD_FAST                'new_shipping_queries'
              608  CALL_METHOD_1         1  ''
              610  POP_TOP          
            612_0  COME_FROM           598  '598'

 L. 399       612  LOAD_FAST                'new_pre_checkout_queries'
          614_616  POP_JUMP_IF_FALSE   628  'to 628'

 L. 400       618  LOAD_FAST                'self'
              620  LOAD_METHOD              process_new_pre_checkout_query
              622  LOAD_FAST                'new_pre_checkout_queries'
              624  CALL_METHOD_1         1  ''
              626  POP_TOP          
            628_0  COME_FROM           614  '614'

 L. 401       628  LOAD_FAST                'new_polls'
          630_632  POP_JUMP_IF_FALSE   644  'to 644'

 L. 402       634  LOAD_FAST                'self'
              636  LOAD_METHOD              process_new_poll
              638  LOAD_FAST                'new_polls'
              640  CALL_METHOD_1         1  ''
              642  POP_TOP          
            644_0  COME_FROM           630  '630'

 L. 403       644  LOAD_FAST                'new_poll_answers'
          646_648  POP_JUMP_IF_FALSE   660  'to 660'

 L. 404       650  LOAD_FAST                'self'
              652  LOAD_METHOD              process_new_poll_answer
              654  LOAD_FAST                'new_poll_answers'
              656  CALL_METHOD_1         1  ''
              658  POP_TOP          
            660_0  COME_FROM           646  '646'

Parse error at or near `<117>' instruction at offset 136

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

    def process_middlewares--- This code section failed: ---

 L. 443         0  LOAD_FAST                'self'
                2  LOAD_ATTR                typed_middleware_handlers
                4  LOAD_METHOD              items
                6  CALL_METHOD_0         0  ''
                8  GET_ITER         
             10_0  COME_FROM            30  '30'
               10  FOR_ITER             60  'to 60'
               12  UNPACK_SEQUENCE_2     2 
               14  STORE_FAST               'update_type'
               16  STORE_FAST               'middlewares'

 L. 444        18  LOAD_GLOBAL              getattr
               20  LOAD_FAST                'update'
               22  LOAD_FAST                'update_type'
               24  CALL_FUNCTION_2       2  ''
               26  LOAD_CONST               None
               28  <117>                 1  ''
               30  POP_JUMP_IF_FALSE    10  'to 10'

 L. 445        32  LOAD_FAST                'middlewares'
               34  GET_ITER         
               36  FOR_ITER             58  'to 58'
               38  STORE_FAST               'typed_middleware_handler'

 L. 446        40  LOAD_FAST                'typed_middleware_handler'
               42  LOAD_FAST                'self'
               44  LOAD_GLOBAL              getattr
               46  LOAD_FAST                'update'
               48  LOAD_FAST                'update_type'
               50  CALL_FUNCTION_2       2  ''
               52  CALL_FUNCTION_2       2  ''
               54  POP_TOP          
               56  JUMP_BACK            36  'to 36'
               58  JUMP_BACK            10  'to 10'

 L. 448        60  LOAD_GLOBAL              len
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                default_middleware_handlers
               66  CALL_FUNCTION_1       1  ''
               68  LOAD_CONST               0
               70  COMPARE_OP               >
               72  POP_JUMP_IF_FALSE    96  'to 96'

 L. 449        74  LOAD_FAST                'self'
               76  LOAD_ATTR                default_middleware_handlers
               78  GET_ITER         
               80  FOR_ITER             96  'to 96'
               82  STORE_FAST               'default_middleware_handler'

 L. 450        84  LOAD_FAST                'default_middleware_handler'
               86  LOAD_FAST                'self'
               88  LOAD_FAST                'update'
               90  CALL_FUNCTION_2       2  ''
               92  POP_TOP          
               94  JUMP_BACK            80  'to 80'
             96_0  COME_FROM            72  '72'

Parse error at or near `<117>' instruction at offset 28

    def __notify_update(self, new_messages):
        if len(self.update_listener) == 0:
            return
        for listener in self.update_listener:
            self._exec_task(listener, new_messages)

    def infinity_polling--- This code section failed: ---

 L. 459         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _TeleBot__stop_polling
                4  LOAD_METHOD              is_set
                6  CALL_METHOD_0         0  ''
                8  POP_JUMP_IF_TRUE    142  'to 142'

 L. 460        10  SETUP_FINALLY        40  'to 40'

 L. 461        12  LOAD_FAST                'self'
               14  LOAD_ATTR                polling
               16  LOAD_FAST                'args'
               18  LOAD_CONST               True
               20  LOAD_FAST                'timeout'
               22  LOAD_FAST                'long_polling_timeout'
               24  LOAD_CONST               ('none_stop', 'timeout', 'long_polling_timeout')
               26  BUILD_CONST_KEY_MAP_3     3 
               28  LOAD_FAST                'kwargs'
               30  <164>                 1  ''
               32  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               34  POP_TOP          
               36  POP_BLOCK        
               38  JUMP_FORWARD        130  'to 130'
             40_0  COME_FROM_FINALLY    10  '10'

 L. 462        40  DUP_TOP          
               42  LOAD_GLOBAL              Exception
               44  <121>               128  ''
               46  POP_TOP          
               48  STORE_FAST               'e'
               50  POP_TOP          
               52  SETUP_FINALLY       120  'to 120'

 L. 463        54  LOAD_GLOBAL              logger
               56  LOAD_METHOD              error
               58  LOAD_STR                 'Infinity polling exception: %s'
               60  LOAD_GLOBAL              str
               62  LOAD_FAST                'e'
               64  CALL_FUNCTION_1       1  ''
               66  CALL_METHOD_2         2  ''
               68  POP_TOP          

 L. 464        70  LOAD_GLOBAL              logger
               72  LOAD_METHOD              debug
               74  LOAD_STR                 'Exception traceback:\n%s'
               76  LOAD_GLOBAL              traceback
               78  LOAD_METHOD              format_exc
               80  CALL_METHOD_0         0  ''
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          

 L. 465        86  LOAD_GLOBAL              time
               88  LOAD_METHOD              sleep
               90  LOAD_CONST               3
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          

 L. 466        96  POP_BLOCK        
               98  POP_EXCEPT       
              100  LOAD_CONST               None
              102  STORE_FAST               'e'
              104  DELETE_FAST              'e'
              106  JUMP_BACK             0  'to 0'
              108  POP_BLOCK        
              110  POP_EXCEPT       
              112  LOAD_CONST               None
              114  STORE_FAST               'e'
              116  DELETE_FAST              'e'
              118  JUMP_FORWARD        130  'to 130'
            120_0  COME_FROM_FINALLY    52  '52'
              120  LOAD_CONST               None
              122  STORE_FAST               'e'
              124  DELETE_FAST              'e'
              126  <48>             
              128  <48>             
            130_0  COME_FROM           118  '118'
            130_1  COME_FROM            38  '38'

 L. 467       130  LOAD_GLOBAL              logger
              132  LOAD_METHOD              info
              134  LOAD_STR                 'Infinity polling: polling exited'
              136  CALL_METHOD_1         1  ''
              138  POP_TOP          
              140  JUMP_BACK             0  'to 0'
            142_0  COME_FROM             8  '8'

 L. 468       142  LOAD_GLOBAL              logger
              144  LOAD_METHOD              info
              146  LOAD_STR                 'Break infinity polling'
              148  CALL_METHOD_1         1  ''
              150  POP_TOP          

Parse error at or near `<164>' instruction at offset 30

    def polling(self, none_stop=False, interval=0, timeout=20, long_polling_timeout=20):
        """
        This function creates a new Thread that calls an internal __retrieve_updates function.
        This allows the bot to retrieve Updates automagically and notify listeners and message handlers accordingly.

        Warning: Do not call this function more than once!

        Always get updates.
        :param interval:
        :param none_stop: Do not stop polling when an ApiException occurs.
        :param timeout: Integer. Request connection timeout
        :param long_polling_timeout. Timeout in seconds for long polling.
        :return:
        """
        if self.threaded:
            self._TeleBot__threaded_polling(none_stop, interval, timeout, long_polling_timeout)
        else:
            self._TeleBot__non_threaded_polling(none_stop, interval, timeout, long_polling_timeout)

    def __threaded_polling--- This code section failed: ---

 L. 490         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              info
                4  LOAD_STR                 'Started polling.'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 491        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _TeleBot__stop_polling
               14  LOAD_METHOD              clear
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 492        20  LOAD_CONST               0.25
               22  STORE_FAST               'error_interval'

 L. 494        24  LOAD_GLOBAL              util
               26  LOAD_ATTR                WorkerThread
               28  LOAD_STR                 'PollingThread'
               30  LOAD_CONST               ('name',)
               32  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               34  STORE_FAST               'polling_thread'

 L. 495        36  LOAD_GLOBAL              util
               38  LOAD_METHOD              OrEvent

 L. 496        40  LOAD_FAST                'polling_thread'
               42  LOAD_ATTR                done_event

 L. 497        44  LOAD_FAST                'polling_thread'
               46  LOAD_ATTR                exception_event

 L. 498        48  LOAD_FAST                'self'
               50  LOAD_ATTR                worker_pool
               52  LOAD_ATTR                exception_event

 L. 495        54  CALL_METHOD_3         3  ''
               56  STORE_FAST               'or_event'

 L. 501        58  LOAD_FAST                'self'
               60  LOAD_ATTR                _TeleBot__stop_polling
               62  LOAD_METHOD              wait
               64  LOAD_FAST                'interval'
               66  CALL_METHOD_1         1  ''
            68_70  POP_JUMP_IF_TRUE    484  'to 484'

 L. 502        72  LOAD_FAST                'or_event'
               74  LOAD_METHOD              clear
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          

 L. 503        80  SETUP_FINALLY       132  'to 132'

 L. 504        82  LOAD_FAST                'polling_thread'
               84  LOAD_METHOD              put
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                _TeleBot__retrieve_updates
               90  LOAD_FAST                'timeout'
               92  LOAD_FAST                'long_polling_timeout'
               94  CALL_METHOD_3         3  ''
               96  POP_TOP          

 L. 505        98  LOAD_FAST                'or_event'
              100  LOAD_METHOD              wait
              102  CALL_METHOD_0         0  ''
              104  POP_TOP          

 L. 506       106  LOAD_FAST                'polling_thread'
              108  LOAD_METHOD              raise_exceptions
              110  CALL_METHOD_0         0  ''
              112  POP_TOP          

 L. 507       114  LOAD_FAST                'self'
              116  LOAD_ATTR                worker_pool
              118  LOAD_METHOD              raise_exceptions
              120  CALL_METHOD_0         0  ''
              122  POP_TOP          

 L. 508       124  LOAD_CONST               0.25
              126  STORE_FAST               'error_interval'
              128  POP_BLOCK        
              130  JUMP_BACK            58  'to 58'
            132_0  COME_FROM_FINALLY    80  '80'

 L. 509       132  DUP_TOP          
              134  LOAD_GLOBAL              apihelper
              136  LOAD_ATTR                ApiException
          138_140  <121>               304  ''
              142  POP_TOP          
              144  STORE_FAST               'e'
              146  POP_TOP          
              148  SETUP_FINALLY       296  'to 296'

 L. 510       150  LOAD_FAST                'self'
              152  LOAD_ATTR                exception_handler
              154  LOAD_CONST               None
              156  <117>                 1  ''
              158  POP_JUMP_IF_FALSE   174  'to 174'

 L. 511       160  LOAD_FAST                'self'
              162  LOAD_ATTR                exception_handler
              164  LOAD_METHOD              handle
              166  LOAD_FAST                'e'
              168  CALL_METHOD_1         1  ''
              170  STORE_FAST               'handled'
              172  JUMP_FORWARD        178  'to 178'
            174_0  COME_FROM           158  '158'

 L. 513       174  LOAD_CONST               False
              176  STORE_FAST               'handled'
            178_0  COME_FROM           172  '172'

 L. 514       178  LOAD_FAST                'handled'
          180_182  POP_JUMP_IF_TRUE    256  'to 256'

 L. 515       184  LOAD_GLOBAL              logger
              186  LOAD_METHOD              error
              188  LOAD_FAST                'e'
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          

 L. 516       194  LOAD_FAST                'non_stop'
              196  POP_JUMP_IF_TRUE    220  'to 220'

 L. 517       198  LOAD_FAST                'self'
              200  LOAD_ATTR                _TeleBot__stop_polling
              202  LOAD_METHOD              set
              204  CALL_METHOD_0         0  ''
              206  POP_TOP          

 L. 518       208  LOAD_GLOBAL              logger
              210  LOAD_METHOD              info
              212  LOAD_STR                 'Exception occurred. Stopping.'
              214  CALL_METHOD_1         1  ''
              216  POP_TOP          
              218  JUMP_FORWARD        254  'to 254'
            220_0  COME_FROM           196  '196'

 L. 522       220  LOAD_GLOBAL              logger
              222  LOAD_METHOD              info
              224  LOAD_STR                 'Waiting for {0} seconds until retry'
              226  LOAD_METHOD              format
              228  LOAD_FAST                'error_interval'
              230  CALL_METHOD_1         1  ''
              232  CALL_METHOD_1         1  ''
              234  POP_TOP          

 L. 523       236  LOAD_GLOBAL              time
              238  LOAD_METHOD              sleep
              240  LOAD_FAST                'error_interval'
              242  CALL_METHOD_1         1  ''
              244  POP_TOP          

 L. 524       246  LOAD_FAST                'error_interval'
              248  LOAD_CONST               2
              250  INPLACE_MULTIPLY 
              252  STORE_FAST               'error_interval'
            254_0  COME_FROM           218  '218'
              254  JUMP_FORWARD        266  'to 266'
            256_0  COME_FROM           180  '180'

 L. 528       256  LOAD_GLOBAL              time
              258  LOAD_METHOD              sleep
              260  LOAD_FAST                'error_interval'
              262  CALL_METHOD_1         1  ''
              264  POP_TOP          
            266_0  COME_FROM           254  '254'

 L. 529       266  LOAD_FAST                'polling_thread'
              268  LOAD_METHOD              clear_exceptions
              270  CALL_METHOD_0         0  ''
              272  POP_TOP          

 L. 530       274  LOAD_FAST                'self'
              276  LOAD_ATTR                worker_pool
              278  LOAD_METHOD              clear_exceptions
              280  CALL_METHOD_0         0  ''
              282  POP_TOP          
              284  POP_BLOCK        
              286  POP_EXCEPT       
              288  LOAD_CONST               None
              290  STORE_FAST               'e'
              292  DELETE_FAST              'e'
              294  JUMP_BACK            58  'to 58'
            296_0  COME_FROM_FINALLY   148  '148'
              296  LOAD_CONST               None
              298  STORE_FAST               'e'
              300  DELETE_FAST              'e'
              302  <48>             

 L. 531       304  DUP_TOP          
              306  LOAD_GLOBAL              KeyboardInterrupt
          308_310  <121>               348  ''
              312  POP_TOP          
              314  POP_TOP          
              316  POP_TOP          

 L. 532       318  LOAD_GLOBAL              logger
              320  LOAD_METHOD              info
              322  LOAD_STR                 'KeyboardInterrupt received.'
              324  CALL_METHOD_1         1  ''
              326  POP_TOP          

 L. 533       328  LOAD_FAST                'self'
              330  LOAD_ATTR                _TeleBot__stop_polling
              332  LOAD_METHOD              set
              334  CALL_METHOD_0         0  ''
              336  POP_TOP          

 L. 534       338  POP_EXCEPT       
          340_342  JUMP_ABSOLUTE       484  'to 484'
              344  POP_EXCEPT       
              346  JUMP_BACK            58  'to 58'

 L. 535       348  DUP_TOP          
              350  LOAD_GLOBAL              Exception
          352_354  <121>               480  ''
              356  POP_TOP          
              358  STORE_FAST               'e'
              360  POP_TOP          
              362  SETUP_FINALLY       472  'to 472'

 L. 536       364  LOAD_FAST                'self'
              366  LOAD_ATTR                exception_handler
              368  LOAD_CONST               None
              370  <117>                 1  ''
          372_374  POP_JUMP_IF_FALSE   390  'to 390'

 L. 537       376  LOAD_FAST                'self'
              378  LOAD_ATTR                exception_handler
              380  LOAD_METHOD              handle
              382  LOAD_FAST                'e'
              384  CALL_METHOD_1         1  ''
              386  STORE_FAST               'handled'
              388  JUMP_FORWARD        394  'to 394'
            390_0  COME_FROM           372  '372'

 L. 539       390  LOAD_CONST               False
              392  STORE_FAST               'handled'
            394_0  COME_FROM           388  '388'

 L. 540       394  LOAD_FAST                'handled'
          396_398  POP_JUMP_IF_TRUE    432  'to 432'

 L. 541       400  LOAD_FAST                'polling_thread'
              402  LOAD_METHOD              stop
              404  CALL_METHOD_0         0  ''
              406  POP_TOP          

 L. 542       408  LOAD_FAST                'polling_thread'
              410  LOAD_METHOD              clear_exceptions
              412  CALL_METHOD_0         0  ''
              414  POP_TOP          

 L. 543       416  LOAD_FAST                'self'
              418  LOAD_ATTR                worker_pool
              420  LOAD_METHOD              clear_exceptions
              422  CALL_METHOD_0         0  ''
              424  POP_TOP          

 L. 544       426  LOAD_FAST                'e'
              428  RAISE_VARARGS_1       1  'exception instance'
              430  JUMP_FORWARD        460  'to 460'
            432_0  COME_FROM           396  '396'

 L. 546       432  LOAD_FAST                'polling_thread'
              434  LOAD_METHOD              clear_exceptions
              436  CALL_METHOD_0         0  ''
              438  POP_TOP          

 L. 547       440  LOAD_FAST                'self'
              442  LOAD_ATTR                worker_pool
              444  LOAD_METHOD              clear_exceptions
              446  CALL_METHOD_0         0  ''
              448  POP_TOP          

 L. 548       450  LOAD_GLOBAL              time
              452  LOAD_METHOD              sleep
              454  LOAD_FAST                'error_interval'
              456  CALL_METHOD_1         1  ''
              458  POP_TOP          
            460_0  COME_FROM           430  '430'
              460  POP_BLOCK        
              462  POP_EXCEPT       
              464  LOAD_CONST               None
              466  STORE_FAST               'e'
              468  DELETE_FAST              'e'
              470  JUMP_BACK            58  'to 58'
            472_0  COME_FROM_FINALLY   362  '362'
              472  LOAD_CONST               None
              474  STORE_FAST               'e'
              476  DELETE_FAST              'e'
              478  <48>             
              480  <48>             
              482  JUMP_BACK            58  'to 58'
            484_0  COME_FROM            68  '68'

 L. 550       484  LOAD_FAST                'polling_thread'
              486  LOAD_METHOD              stop
              488  CALL_METHOD_0         0  ''
              490  POP_TOP          

 L. 551       492  LOAD_FAST                'polling_thread'
              494  LOAD_METHOD              clear_exceptions
              496  CALL_METHOD_0         0  ''
              498  POP_TOP          

 L. 552       500  LOAD_FAST                'self'
              502  LOAD_ATTR                worker_pool
              504  LOAD_METHOD              clear_exceptions
              506  CALL_METHOD_0         0  ''
              508  POP_TOP          

 L. 553       510  LOAD_GLOBAL              logger
              512  LOAD_METHOD              info
              514  LOAD_STR                 'Stopped polling.'
              516  CALL_METHOD_1         1  ''
              518  POP_TOP          

Parse error at or near `<121>' instruction at offset 138_140

    def __non_threaded_polling--- This code section failed: ---

 L. 556         0  LOAD_GLOBAL              logger
                2  LOAD_METHOD              info
                4  LOAD_STR                 'Started polling.'
                6  CALL_METHOD_1         1  ''
                8  POP_TOP          

 L. 557        10  LOAD_FAST                'self'
               12  LOAD_ATTR                _TeleBot__stop_polling
               14  LOAD_METHOD              clear
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 558        20  LOAD_CONST               0.25
               22  STORE_FAST               'error_interval'

 L. 560        24  LOAD_FAST                'self'
               26  LOAD_ATTR                _TeleBot__stop_polling
               28  LOAD_METHOD              wait
               30  LOAD_FAST                'interval'
               32  CALL_METHOD_1         1  ''
            34_36  POP_JUMP_IF_TRUE    344  'to 344'

 L. 561        38  SETUP_FINALLY        60  'to 60'

 L. 562        40  LOAD_FAST                'self'
               42  LOAD_METHOD              _TeleBot__retrieve_updates
               44  LOAD_FAST                'timeout'
               46  LOAD_FAST                'long_polling_timeout'
               48  CALL_METHOD_2         2  ''
               50  POP_TOP          

 L. 563        52  LOAD_CONST               0.25
               54  STORE_FAST               'error_interval'
               56  POP_BLOCK        
               58  JUMP_BACK            24  'to 24'
             60_0  COME_FROM_FINALLY    38  '38'

 L. 564        60  DUP_TOP          
               62  LOAD_GLOBAL              apihelper
               64  LOAD_ATTR                ApiException
               66  <121>               210  ''
               68  POP_TOP          
               70  STORE_FAST               'e'
               72  POP_TOP          
               74  SETUP_FINALLY       202  'to 202'

 L. 565        76  LOAD_FAST                'self'
               78  LOAD_ATTR                exception_handler
               80  LOAD_CONST               None
               82  <117>                 1  ''
               84  POP_JUMP_IF_FALSE   100  'to 100'

 L. 566        86  LOAD_FAST                'self'
               88  LOAD_ATTR                exception_handler
               90  LOAD_METHOD              handle
               92  LOAD_FAST                'e'
               94  CALL_METHOD_1         1  ''
               96  STORE_FAST               'handled'
               98  JUMP_FORWARD        104  'to 104'
            100_0  COME_FROM            84  '84'

 L. 568       100  LOAD_CONST               False
              102  STORE_FAST               'handled'
            104_0  COME_FROM            98  '98'

 L. 570       104  LOAD_FAST                'handled'
              106  POP_JUMP_IF_TRUE    180  'to 180'

 L. 571       108  LOAD_GLOBAL              logger
              110  LOAD_METHOD              error
              112  LOAD_FAST                'e'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L. 572       118  LOAD_FAST                'non_stop'
              120  POP_JUMP_IF_TRUE    144  'to 144'

 L. 573       122  LOAD_FAST                'self'
              124  LOAD_ATTR                _TeleBot__stop_polling
              126  LOAD_METHOD              set
              128  CALL_METHOD_0         0  ''
              130  POP_TOP          

 L. 574       132  LOAD_GLOBAL              logger
              134  LOAD_METHOD              info
              136  LOAD_STR                 'Exception occurred. Stopping.'
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
              142  JUMP_ABSOLUTE       190  'to 190'
            144_0  COME_FROM           120  '120'

 L. 576       144  LOAD_GLOBAL              logger
              146  LOAD_METHOD              info
              148  LOAD_STR                 'Waiting for {0} seconds until retry'
              150  LOAD_METHOD              format
              152  LOAD_FAST                'error_interval'
              154  CALL_METHOD_1         1  ''
              156  CALL_METHOD_1         1  ''
              158  POP_TOP          

 L. 577       160  LOAD_GLOBAL              time
              162  LOAD_METHOD              sleep
              164  LOAD_FAST                'error_interval'
              166  CALL_METHOD_1         1  ''
              168  POP_TOP          

 L. 578       170  LOAD_FAST                'error_interval'
              172  LOAD_CONST               2
              174  INPLACE_MULTIPLY 
              176  STORE_FAST               'error_interval'
              178  JUMP_FORWARD        190  'to 190'
            180_0  COME_FROM           106  '106'

 L. 580       180  LOAD_GLOBAL              time
              182  LOAD_METHOD              sleep
              184  LOAD_FAST                'error_interval'
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          
            190_0  COME_FROM           178  '178'
              190  POP_BLOCK        
              192  POP_EXCEPT       
              194  LOAD_CONST               None
              196  STORE_FAST               'e'
              198  DELETE_FAST              'e'
              200  JUMP_BACK            24  'to 24'
            202_0  COME_FROM_FINALLY    74  '74'
              202  LOAD_CONST               None
              204  STORE_FAST               'e'
              206  DELETE_FAST              'e'
              208  <48>             

 L. 581       210  DUP_TOP          
              212  LOAD_GLOBAL              KeyboardInterrupt
              214  <121>               252  ''
              216  POP_TOP          
              218  POP_TOP          
              220  POP_TOP          

 L. 582       222  LOAD_GLOBAL              logger
              224  LOAD_METHOD              info
              226  LOAD_STR                 'KeyboardInterrupt received.'
              228  CALL_METHOD_1         1  ''
              230  POP_TOP          

 L. 583       232  LOAD_FAST                'self'
              234  LOAD_ATTR                _TeleBot__stop_polling
              236  LOAD_METHOD              set
              238  CALL_METHOD_0         0  ''
              240  POP_TOP          

 L. 584       242  POP_EXCEPT       
          244_246  JUMP_ABSOLUTE       344  'to 344'
              248  POP_EXCEPT       
              250  JUMP_BACK            24  'to 24'

 L. 585       252  DUP_TOP          
              254  LOAD_GLOBAL              Exception
          256_258  <121>               340  ''
              260  POP_TOP          
              262  STORE_FAST               'e'
              264  POP_TOP          
              266  SETUP_FINALLY       332  'to 332'

 L. 586       268  LOAD_FAST                'self'
              270  LOAD_ATTR                exception_handler
              272  LOAD_CONST               None
              274  <117>                 1  ''
          276_278  POP_JUMP_IF_FALSE   294  'to 294'

 L. 587       280  LOAD_FAST                'self'
              282  LOAD_ATTR                exception_handler
              284  LOAD_METHOD              handle
              286  LOAD_FAST                'e'
              288  CALL_METHOD_1         1  ''
              290  STORE_FAST               'handled'
              292  JUMP_FORWARD        298  'to 298'
            294_0  COME_FROM           276  '276'

 L. 589       294  LOAD_CONST               False
              296  STORE_FAST               'handled'
            298_0  COME_FROM           292  '292'

 L. 590       298  LOAD_FAST                'handled'
          300_302  POP_JUMP_IF_TRUE    310  'to 310'

 L. 591       304  LOAD_FAST                'e'
              306  RAISE_VARARGS_1       1  'exception instance'
              308  JUMP_FORWARD        320  'to 320'
            310_0  COME_FROM           300  '300'

 L. 593       310  LOAD_GLOBAL              time
              312  LOAD_METHOD              sleep
              314  LOAD_FAST                'error_interval'
              316  CALL_METHOD_1         1  ''
              318  POP_TOP          
            320_0  COME_FROM           308  '308'
              320  POP_BLOCK        
              322  POP_EXCEPT       
              324  LOAD_CONST               None
              326  STORE_FAST               'e'
              328  DELETE_FAST              'e'
              330  JUMP_BACK            24  'to 24'
            332_0  COME_FROM_FINALLY   266  '266'
              332  LOAD_CONST               None
              334  STORE_FAST               'e'
              336  DELETE_FAST              'e'
              338  <48>             
              340  <48>             
              342  JUMP_BACK            24  'to 24'
            344_0  COME_FROM            34  '34'

 L. 595       344  LOAD_GLOBAL              logger
              346  LOAD_METHOD              info
              348  LOAD_STR                 'Stopped polling.'
              350  CALL_METHOD_1         1  ''
              352  POP_TOP          

Parse error at or near `<121>' instruction at offset 66

    def _exec_task--- This code section failed: ---

 L. 598         0  LOAD_FAST                'self'
                2  LOAD_ATTR                threaded
                4  POP_JUMP_IF_FALSE    34  'to 34'

 L. 599         6  LOAD_FAST                'self'
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

 L. 601        34  LOAD_FAST                'task'
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

    def get_me(self):
        result = apihelper.get_me(self.token)
        return types.User.de_json(result)

    def get_file(self, file_id):
        return types.File.de_json(apihelper.get_file(self.token, file_id))

    def get_file_url(self, file_id):
        return apihelper.get_file_url(self.token, file_id)

    def download_file(self, file_path):
        return apihelper.download_file(self.token, file_path)

    def get_user_profile_photos(self, user_id, offset=None, limit=None):
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

    def get_chat(self, chat_id):
        """
        Use this method to get up to date information about the chat (current name of the user for one-on-one
        conversations, current username of a user, group or channel, etc.). Returns a Chat object on success.
        :param chat_id:
        :return:
        """
        result = apihelper.get_chat(self.token, chat_id)
        return types.Chat.de_json(result)

    def leave_chat(self, chat_id):
        """
        Use this method for your bot to leave a group, supergroup or channel. Returns True on success.
        :param chat_id:
        :return:
        """
        result = apihelper.leave_chat(self.token, chat_id)
        return result

    def get_chat_administrators(self, chat_id):
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

    def get_chat_members_count(self, chat_id):
        """
        Use this method to get the number of members in a chat. Returns Int on success.
        :param chat_id:
        :return:
        """
        result = apihelper.get_chat_members_count(self.token, chat_id)
        return result

    def set_chat_sticker_set(self, chat_id, sticker_set_name):
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

    def delete_chat_sticker_set(self, chat_id):
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

    def get_chat_member(self, chat_id, user_id):
        """
        Use this method to get information about a member of a chat. Returns a ChatMember object on success.
        :param chat_id:
        :param user_id:
        :return:
        """
        result = apihelper.get_chat_member(self.token, chat_id, user_id)
        return types.ChatMember.de_json(result)

    def send_message--- This code section failed: ---

 L. 736         0  LOAD_FAST                'parse_mode'
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

 L. 738        18  LOAD_GLOBAL              types
               20  LOAD_ATTR                Message
               22  LOAD_METHOD              de_json

 L. 739        24  LOAD_GLOBAL              apihelper
               26  LOAD_METHOD              send_message
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                token
               32  LOAD_FAST                'chat_id'
               34  LOAD_FAST                'text'
               36  LOAD_FAST                'disable_web_page_preview'
               38  LOAD_FAST                'reply_to_message_id'

 L. 740        40  LOAD_FAST                'reply_markup'
               42  LOAD_FAST                'parse_mode'
               44  LOAD_FAST                'disable_notification'
               46  LOAD_FAST                'timeout'

 L. 739        48  CALL_METHOD_9         9  ''

 L. 738        50  CALL_METHOD_1         1  ''
               52  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def forward_message(self, chat_id, from_chat_id, message_id, disable_notification=None, timeout=None):
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

    def delete_message(self, chat_id, message_id, timeout=None):
        """
        Use this method to delete message. Returns True on success.
        :param chat_id: in which chat to delete
        :param message_id: which message to delete
        :param timeout:
        :return: API reply.
        """
        return apihelper.delete_message(self.token, chat_id, message_id, timeout)

    def send_dice(self, chat_id, emoji=None, disable_notification=None, reply_to_message_id=None, reply_markup=None, timeout=None):
        """
        Use this method to send dices.
        :param chat_id:
        :param emoji:
        :param disable_notification:
        :param reply_to_message_id:
        :param reply_markup:
        :param timeout:
        :return: Message
        """
        return types.Message.de_json(apihelper.send_dice(self.token, chat_id, emoji, disable_notification, reply_to_message_id, reply_markup, timeout))

    def send_photo--- This code section failed: ---

 L. 799         0  LOAD_FAST                'parse_mode'
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

 L. 801        18  LOAD_GLOBAL              types
               20  LOAD_ATTR                Message
               22  LOAD_METHOD              de_json

 L. 802        24  LOAD_GLOBAL              apihelper
               26  LOAD_METHOD              send_photo
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                token
               32  LOAD_FAST                'chat_id'
               34  LOAD_FAST                'photo'
               36  LOAD_FAST                'caption'
               38  LOAD_FAST                'reply_to_message_id'
               40  LOAD_FAST                'reply_markup'

 L. 803        42  LOAD_FAST                'parse_mode'
               44  LOAD_FAST                'disable_notification'
               46  LOAD_FAST                'timeout'

 L. 802        48  CALL_METHOD_9         9  ''

 L. 801        50  CALL_METHOD_1         1  ''
               52  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def send_audio--- This code section failed: ---

 L. 824         0  LOAD_FAST                'parse_mode'
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

 L. 826        18  LOAD_GLOBAL              types
               20  LOAD_ATTR                Message
               22  LOAD_METHOD              de_json

 L. 827        24  LOAD_GLOBAL              apihelper
               26  LOAD_METHOD              send_audio
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                token
               32  LOAD_FAST                'chat_id'
               34  LOAD_FAST                'audio'
               36  LOAD_FAST                'caption'
               38  LOAD_FAST                'duration'
               40  LOAD_FAST                'performer'
               42  LOAD_FAST                'title'
               44  LOAD_FAST                'reply_to_message_id'

 L. 828        46  LOAD_FAST                'reply_markup'
               48  LOAD_FAST                'parse_mode'
               50  LOAD_FAST                'disable_notification'
               52  LOAD_FAST                'timeout'
               54  LOAD_FAST                'thumb'

 L. 827        56  CALL_METHOD_13       13  ''

 L. 826        58  CALL_METHOD_1         1  ''
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def send_voice--- This code section failed: ---

 L. 845         0  LOAD_FAST                'parse_mode'
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

 L. 847        18  LOAD_GLOBAL              types
               20  LOAD_ATTR                Message
               22  LOAD_METHOD              de_json

 L. 848        24  LOAD_GLOBAL              apihelper
               26  LOAD_METHOD              send_voice
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                token
               32  LOAD_FAST                'chat_id'
               34  LOAD_FAST                'voice'
               36  LOAD_FAST                'caption'
               38  LOAD_FAST                'duration'
               40  LOAD_FAST                'reply_to_message_id'
               42  LOAD_FAST                'reply_markup'

 L. 849        44  LOAD_FAST                'parse_mode'
               46  LOAD_FAST                'disable_notification'
               48  LOAD_FAST                'timeout'

 L. 848        50  CALL_METHOD_10       10  ''

 L. 847        52  CALL_METHOD_1         1  ''
               54  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def send_document--- This code section failed: ---

 L. 866         0  LOAD_FAST                'parse_mode'
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

 L. 868        18  LOAD_GLOBAL              types
               20  LOAD_ATTR                Message
               22  LOAD_METHOD              de_json

 L. 869        24  LOAD_GLOBAL              apihelper
               26  LOAD_METHOD              send_data
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                token
               32  LOAD_FAST                'chat_id'
               34  LOAD_FAST                'data'
               36  LOAD_STR                 'document'
               38  LOAD_FAST                'reply_to_message_id'
               40  LOAD_FAST                'reply_markup'

 L. 870        42  LOAD_FAST                'parse_mode'
               44  LOAD_FAST                'disable_notification'
               46  LOAD_FAST                'timeout'
               48  LOAD_FAST                'caption'
               50  LOAD_FAST                'thumb'

 L. 869        52  CALL_METHOD_11       11  ''

 L. 868        54  CALL_METHOD_1         1  ''
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def send_sticker(self, chat_id, data, reply_to_message_id=None, reply_markup=None, disable_notification=None, timeout=None):
        """
        Use this method to send .webp stickers.
        :param chat_id:
        :param data:
        :param reply_to_message_id:
        :param reply_markup:
        :param disable_notification: to disable the notification
        :param timeout: timeout
        :return: API reply.
        """
        return types.Message.de_json(apihelper.send_data(self.token, chat_id, data, 'sticker', reply_to_message_id, reply_markup, disable_notification, timeout))

    def send_video--- This code section failed: ---

 L. 909         0  LOAD_FAST                'parse_mode'
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

 L. 911        18  LOAD_GLOBAL              types
               20  LOAD_ATTR                Message
               22  LOAD_METHOD              de_json

 L. 912        24  LOAD_GLOBAL              apihelper
               26  LOAD_METHOD              send_video
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                token
               32  LOAD_FAST                'chat_id'
               34  LOAD_FAST                'data'
               36  LOAD_FAST                'duration'
               38  LOAD_FAST                'caption'
               40  LOAD_FAST                'reply_to_message_id'
               42  LOAD_FAST                'reply_markup'

 L. 913        44  LOAD_FAST                'parse_mode'
               46  LOAD_FAST                'supports_streaming'
               48  LOAD_FAST                'disable_notification'
               50  LOAD_FAST                'timeout'
               52  LOAD_FAST                'thumb'
               54  LOAD_FAST                'width'
               56  LOAD_FAST                'height'

 L. 912        58  CALL_METHOD_14       14  ''

 L. 911        60  CALL_METHOD_1         1  ''
               62  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def send_animation--- This code section failed: ---

 L. 933         0  LOAD_FAST                'parse_mode'
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

 L. 935        18  LOAD_GLOBAL              types
               20  LOAD_ATTR                Message
               22  LOAD_METHOD              de_json

 L. 936        24  LOAD_GLOBAL              apihelper
               26  LOAD_METHOD              send_animation
               28  LOAD_FAST                'self'
               30  LOAD_ATTR                token
               32  LOAD_FAST                'chat_id'
               34  LOAD_FAST                'animation'
               36  LOAD_FAST                'duration'
               38  LOAD_FAST                'caption'
               40  LOAD_FAST                'reply_to_message_id'
               42  LOAD_FAST                'reply_markup'

 L. 937        44  LOAD_FAST                'parse_mode'
               46  LOAD_FAST                'disable_notification'
               48  LOAD_FAST                'timeout'
               50  LOAD_FAST                'thumb'

 L. 936        52  CALL_METHOD_11       11  ''

 L. 935        54  CALL_METHOD_1         1  ''
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def send_video_note(self, chat_id, data, duration=None, length=None, reply_to_message_id=None, reply_markup=None, disable_notification=None, timeout=None, thumb=None):
        """
        As of v.4.0, Telegram clients support rounded square mp4 videos of up to 1 minute long. Use this method to send video messages.
        :param chat_id: Integer : Unique identifier for the message recipient — User or GroupChat id
        :param data: InputFile or String : Video note to send. You can either pass a file_id as String to resend a video that is already on the Telegram server
        :param duration: Integer : Duration of sent video in seconds
        :param length: Integer : Video width and height, Can't be None and should be in range of (0, 640)
        :param reply_to_message_id:
        :param reply_markup:
        :param disable_notification:
        :param timeout:
        :param thumb: InputFile or String : Thumbnail of the file sent
        :return:
        """
        return types.Message.de_json(apihelper.send_video_noteself.tokenchat_iddatadurationlengthreply_to_message_idreply_markupdisable_notificationtimeoutthumb)

    def send_media_group(self, chat_id, media, disable_notification=None, reply_to_message_id=None, timeout=None):
        """
        send a group of photos or videos as an album. On success, an array of the sent Messages is returned.
        :param chat_id:
        :param media:
        :param disable_notification:
        :param reply_to_message_id:
        :param timeout:
        :return:
        """
        result = apihelper.send_media_group(self.token, chat_id, media, disable_notification, reply_to_message_id, timeout)
        ret = []
        for msg in result:
            ret.append(types.Message.de_json(msg))
        else:
            return ret

    def send_location(self, chat_id, latitude, longitude, live_period=None, reply_to_message_id=None, reply_markup=None, disable_notification=None, timeout=None):
        """
        Use this method to send point on the map.
        :param chat_id:
        :param latitude:
        :param longitude:
        :param live_period
        :param reply_to_message_id:
        :param reply_markup:
        :param disable_notification:
        :param timeout:
        :return: API reply.
        """
        return types.Message.de_json(apihelper.send_locationself.tokenchat_idlatitudelongitudelive_periodreply_to_message_idreply_markupdisable_notificationtimeout)

    def edit_message_live_location(self, latitude, longitude, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None, timeout=None):
        """
        Use this method to edit live location
        :param latitude:
        :param longitude:
        :param chat_id:
        :param message_id:
        :param inline_message_id:
        :param reply_markup:
        :param timeout:
        :return:
        """
        return types.Message.de_json(apihelper.edit_message_live_location(self.token, latitude, longitude, chat_id, message_id, inline_message_id, reply_markup, timeout))

    def stop_message_live_location(self, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None, timeout=None):
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

    def send_venue(self, chat_id, latitude, longitude, title, address, foursquare_id=None, foursquare_type=None, disable_notification=None, reply_to_message_id=None, reply_markup=None, timeout=None):
        """
        Use this method to send information about a venue.
        :param chat_id: Integer or String : Unique identifier for the target chat or username of the target channel
        :param latitude: Float : Latitude of the venue
        :param longitude: Float : Longitude of the venue
        :param title: String : Name of the venue
        :param address: String : Address of the venue
        :param foursquare_id: String : Foursquare identifier of the venue
        :param foursquare_type: Foursquare type of the venue, if known. (For example, “arts_entertainment/default”, “arts_entertainment/aquarium” or “food/icecream”.)
        :param disable_notification:
        :param reply_to_message_id:
        :param reply_markup:
        :param timeout:
        :return:
        """
        return types.Message.de_json(apihelper.send_venue(self.token, chat_id, latitude, longitude, title, address, foursquare_id, foursquare_type, disable_notification, reply_to_message_id, reply_markup, timeout))

    def send_contact(self, chat_id, phone_number, first_name, last_name=None, vcard=None, disable_notification=None, reply_to_message_id=None, reply_markup=None, timeout=None):
        return types.Message.de_json(apihelper.send_contactself.tokenchat_idphone_numberfirst_namelast_namevcarddisable_notificationreply_to_message_idreply_markuptimeout)

    def send_chat_action(self, chat_id, action, timeout=None):
        """
        Use this method when you need to tell the user that something is happening on the bot's side.
        The status is set for 5 seconds or less (when a message arrives from your bot, Telegram clients clear
        its typing status).
        :param chat_id:
        :param action:  One of the following strings: 'typing', 'upload_photo', 'record_video', 'upload_video',
                        'record_audio', 'upload_audio', 'upload_document', 'find_location', 'record_video_note', 'upload_video_note'.
        :param timeout:
        :return: API reply. :type: boolean
        """
        return apihelper.send_chat_action(self.token, chat_id, action, timeout)

    def kick_chat_member(self, chat_id, user_id, until_date=None):
        """
        Use this method to kick a user from a group or a supergroup.
        :param chat_id: Int or string : Unique identifier for the target group or username of the target supergroup
        :param user_id: Int : Unique identifier of the target user
        :param until_date: Date when the user will be unbanned, unix time. If user is banned for more than 366 days or
               less than 30 seconds from the current time they are considered to be banned forever
        :return: boolean
        """
        return apihelper.kick_chat_member(self.token, chat_id, user_id, until_date)

    def unban_chat_member(self, chat_id, user_id, only_if_banned=False):
        """
        Use this method to unban a previously kicked user in a supergroup or channel.
        The user will not return to the group or channel automatically, but will be able to join via link, etc.
        The bot must be an administrator for this to work. By default, this method guarantees that after the call
        the user is not a member of the chat, but will be able to join it. So if the user is a member of the chat
        they will also be removed from the chat. If you don't want this, use the parameter only_if_banned.

        :param chat_id: Unique identifier for the target group or username of the target supergroup or channel (in the format @username)
        :param user_id: Unique identifier of the target user
        :param only_if_banned: Do nothing if the user is not banned
        :return: True on success
        """
        return apihelper.unban_chat_member(self.token, chat_id, user_id, only_if_banned)

    def restrict_chat_member(self, chat_id, user_id, until_date=None, can_send_messages=None, can_send_media_messages=None, can_send_polls=None, can_send_other_messages=None, can_add_web_page_previews=None, can_change_info=None, can_invite_users=None, can_pin_messages=None):
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
        :param can_change_info: Pass True, if the user is allowed to change the chat title, photo and other settings. Ignored in public supergroups
        :param can_invite_users: Pass True, if the user is allowed to invite new users to the chat,
                implies can_invite_users
        :param can_pin_messages: Pass True, if the user is allowed to pin messages. Ignored in public supergroups
        :return: True on success
        """
        return apihelper.restrict_chat_member(self.token, chat_id, user_id, until_date, can_send_messages, can_send_media_messages, can_send_polls, can_send_other_messages, can_add_web_page_previews, can_change_info, can_invite_users, can_pin_messages)

    def promote_chat_member(self, chat_id, user_id, can_change_info=None, can_post_messages=None, can_edit_messages=None, can_delete_messages=None, can_invite_users=None, can_restrict_members=None, can_pin_messages=None, can_promote_members=None):
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
        :return: True on success.
        """
        return apihelper.promote_chat_memberself.tokenchat_iduser_idcan_change_infocan_post_messagescan_edit_messagescan_delete_messagescan_invite_userscan_restrict_memberscan_pin_messagescan_promote_members

    def set_chat_administrator_custom_title(self, chat_id, user_id, custom_title):
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

    def set_chat_permissions(self, chat_id, permissions):
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

    def export_chat_invite_link(self, chat_id):
        """
        Use this method to export an invite link to a supergroup or a channel. The bot must be an administrator
        in the chat for this to work and must have the appropriate admin rights.

        :param chat_id: Id: Unique identifier for the target chat or username of the target channel
            (in the format @channelusername)
        :return: exported invite link as String on success.
        """
        return apihelper.export_chat_invite_link(self.token, chat_id)

    def set_chat_photo(self, chat_id, photo):
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

    def delete_chat_photo(self, chat_id):
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

    def set_my_commands(self, commands):
        """
        Use this method to change the list of the bot's commands.
        :param commands: Array of BotCommand. A JSON-serialized list of bot commands
            to be set as the list of the bot's commands. At most 100 commands can be specified.
        :return:
        """
        return apihelper.set_my_commands(self.token, commands)

    def set_chat_title(self, chat_id, title):
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

    def set_chat_description(self, chat_id, description=None):
        """
        Use this method to change the description of a supergroup or a channel.
        The bot must be an administrator in the chat for this to work and must have the appropriate admin rights.

        :param chat_id: Int or Str: Unique identifier for the target chat or username of the target channel
            (in the format @channelusername)
        :param description: Str: New chat description, 0-255 characters
        :return: True on success.
        """
        return apihelper.set_chat_description(self.token, chat_id, description)

    def pin_chat_message(self, chat_id, message_id, disable_notification=False):
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

    def unpin_chat_message(self, chat_id, message_id=None):
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

    def unpin_all_chat_messages(self, chat_id):
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

 L.1320         0  LOAD_FAST                'parse_mode'
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

 L.1322        18  LOAD_GLOBAL              apihelper
               20  LOAD_METHOD              edit_message_text
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                token
               26  LOAD_FAST                'text'
               28  LOAD_FAST                'chat_id'
               30  LOAD_FAST                'message_id'
               32  LOAD_FAST                'inline_message_id'
               34  LOAD_FAST                'parse_mode'

 L.1323        36  LOAD_FAST                'disable_web_page_preview'
               38  LOAD_FAST                'reply_markup'

 L.1322        40  CALL_METHOD_8         8  ''
               42  STORE_FAST               'result'

 L.1324        44  LOAD_GLOBAL              type
               46  LOAD_FAST                'result'
               48  CALL_FUNCTION_1       1  ''
               50  LOAD_GLOBAL              bool
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    60  'to 60'

 L.1325        56  LOAD_FAST                'result'
               58  RETURN_VALUE     
             60_0  COME_FROM            54  '54'

 L.1326        60  LOAD_GLOBAL              types
               62  LOAD_ATTR                Message
               64  LOAD_METHOD              de_json
               66  LOAD_FAST                'result'
               68  CALL_METHOD_1         1  ''
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def edit_message_media(self, media, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
        """
        Use this method to edit animation, audio, document, photo, or video messages. If a message is a part of a message album, then it can be edited only to a photo or a video. Otherwise, message type can be changed arbitrarily. When inline message is edited, new file can't be uploaded. Use previously uploaded file via its file_id or specify a URL.
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

    def edit_message_reply_markup(self, chat_id=None, message_id=None, inline_message_id=None, reply_markup=None):
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

    def send_game(self, chat_id, game_short_name, disable_notification=None, reply_to_message_id=None, reply_markup=None, timeout=None):
        """
        Used to send the game
        :param chat_id:
        :param game_short_name:
        :param disable_notification:
        :param reply_to_message_id:
        :param reply_markup:
        :param timeout:
        :return:
        """
        result = apihelper.send_game(self.token, chat_id, game_short_name, disable_notification, reply_to_message_id, reply_markup, timeout)
        return types.Message.de_json(result)

    def set_game_score(self, user_id, score, force=None, chat_id=None, message_id=None, inline_message_id=None, edit_message=None):
        """
        Sets the value of points in the game to a specific user
        :param user_id:
        :param score:
        :param force:
        :param chat_id:
        :param message_id:
        :param inline_message_id:
        :param edit_message:
        :return:
        """
        result = apihelper.set_game_score(self.token, user_id, score, force, chat_id, message_id, inline_message_id, edit_message)
        if type(result) == bool:
            return result
        return types.Message.de_json(result)

    def get_game_high_scores(self, user_id, chat_id=None, message_id=None, inline_message_id=None):
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

    def send_invoice(self, chat_id, title, description, invoice_payload, provider_token, currency, prices, start_parameter, photo_url=None, photo_size=None, photo_width=None, photo_height=None, need_name=None, need_phone_number=None, need_email=None, need_shipping_address=None, send_phone_number_to_provider=None, send_email_to_provider=None, is_flexible=None, disable_notification=None, reply_to_message_id=None, reply_markup=None, provider_data=None, timeout=None):
        """
        Sends invoice
        :param chat_id: Unique identifier for the target private chat
        :param title: Product name
        :param description: Product description
        :param invoice_payload: Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use for your internal processes.
        :param provider_token: Payments provider token, obtained via @Botfather
        :param currency: Three-letter ISO 4217 currency code, see https://core.telegram.org/bots/payments#supported-currencies
        :param prices: Price breakdown, a list of components (e.g. product price, tax, discount, delivery cost, delivery tax, bonus, etc.)
        :param start_parameter: Unique deep-linking parameter that can be used to generate this invoice when used as a start parameter
        :param photo_url: URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service. People like it better when they see what they are paying for.
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
        :param reply_markup: A JSON-serialized object for an inline keyboard. If empty, one 'Pay total price' button will be shown. If not empty, the first button must be a Pay button
        :param provider_data: A JSON-serialized data about the invoice, which will be shared with the payment provider. A detailed description of required fields should be provided by the payment provider.
        :param timeout:
        :return:
        """
        result = apihelper.send_invoice(self.token, chat_id, title, description, invoice_payload, provider_token, currency, prices, start_parameter, photo_url, photo_size, photo_width, photo_height, need_name, need_phone_number, need_email, need_shipping_address, send_phone_number_to_provider, send_email_to_provider, is_flexible, disable_notification, reply_to_message_id, reply_markup, provider_data, timeout)
        return types.Message.de_json(result)

    def send_poll(self, chat_id, question, options, is_anonymous=None, type=None, allows_multiple_answers=None, correct_option_id=None, explanation=None, explanation_parse_mode=None, open_period=None, close_date=None, is_closed=None, disable_notifications=False, reply_to_message_id=None, reply_markup=None, timeout=None):
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
        :param reply_markup:
        :param timeout:
        :return:
        """
        if isinstance(question, types.Poll):
            raise RuntimeError('The send_poll signature was changed, please see send_poll function details.')
        return types.Message.de_json(apihelper.send_poll(self.token, chat_id, question, options, is_anonymous, type, allows_multiple_answers, correct_option_id, explanation, explanation_parse_mode, open_period, close_date, is_closed, disable_notifications, reply_to_message_id, reply_markup, timeout))

    def stop_poll(self, chat_id, message_id, reply_markup=None):
        """
        Stops poll
        :param chat_id:
        :param message_id:
        :param reply_markup:
        :return:
        """
        return types.Poll.de_json(apihelper.stop_poll(self.token, chat_id, message_id, reply_markup))

    def answer_shipping_query(self, shipping_query_id, ok, shipping_options=None, error_message=None):
        """
        Asks for an answer to a shipping question
        :param shipping_query_id:
        :param ok:
        :param shipping_options:
        :param error_message:
        :return:
        """
        return apihelper.answer_shipping_query(self.token, shipping_query_id, ok, shipping_options, error_message)

    def answer_pre_checkout_query(self, pre_checkout_query_id, ok, error_message=None):
        """
        Response to a request for pre-inspection
        :param pre_checkout_query_id:
        :param ok:
        :param error_message:
        :return:
            """
        return apihelper.answer_pre_checkout_query(self.token, pre_checkout_query_id, ok, error_message)

    def edit_message_caption--- This code section failed: ---

 L.1530         0  LOAD_FAST                'parse_mode'
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

 L.1532        18  LOAD_GLOBAL              apihelper
               20  LOAD_METHOD              edit_message_caption
               22  LOAD_FAST                'self'
               24  LOAD_ATTR                token
               26  LOAD_FAST                'caption'
               28  LOAD_FAST                'chat_id'
               30  LOAD_FAST                'message_id'
               32  LOAD_FAST                'inline_message_id'

 L.1533        34  LOAD_FAST                'parse_mode'
               36  LOAD_FAST                'reply_markup'

 L.1532        38  CALL_METHOD_7         7  ''
               40  STORE_FAST               'result'

 L.1534        42  LOAD_GLOBAL              type
               44  LOAD_FAST                'result'
               46  CALL_FUNCTION_1       1  ''
               48  LOAD_GLOBAL              bool
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    58  'to 58'

 L.1535        54  LOAD_FAST                'result'
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L.1536        58  LOAD_GLOBAL              types
               60  LOAD_ATTR                Message
               62  LOAD_METHOD              de_json
               64  LOAD_FAST                'result'
               66  CALL_METHOD_1         1  ''
               68  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1

    def reply_to--- This code section failed: ---

 L.1546         0  LOAD_FAST                'self'
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

    def answer_inline_query(self, inline_query_id, results, cache_time=None, is_personal=None, next_offset=None, switch_pm_text=None, switch_pm_parameter=None):
        """
        Use this method to send answers to an inline query. On success, True is returned.
        No more than 50 results per query are allowed.
        :param inline_query_id: Unique identifier for the answered query
        :param results: Array of results for the inline query
        :param cache_time: The maximum amount of time in seconds that the result of the inline query may be cached on the server.
        :param is_personal: Pass True, if results may be cached on the server side only for the user that sent the query.
        :param next_offset: Pass the offset that a client should send in the next query with the same text to receive more results.
        :param switch_pm_parameter: If passed, clients will display a button with specified text that switches the user
         to a private chat with the bot and sends the bot a start message with the parameter switch_pm_parameter
        :param switch_pm_text:  Parameter for the start message sent to the bot when user presses the switch button
        :return: True means success.
        """
        return apihelper.answer_inline_query(self.token, inline_query_id, results, cache_time, is_personal, next_offset, switch_pm_text, switch_pm_parameter)

    def answer_callback_query(self, callback_query_id, text=None, show_alert=None, url=None, cache_time=None):
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

    def get_sticker_set(self, name):
        """
        Use this method to get a sticker set. On success, a StickerSet object is returned.
        :param name:
        :return:
        """
        result = apihelper.get_sticker_set(self.token, name)
        return types.StickerSet.de_json(result)

    def upload_sticker_file(self, user_id, png_sticker):
        """
        Use this method to upload a .png file with a sticker for later use in createNewStickerSet and addStickerToSet
        methods (can be used multiple times). Returns the uploaded File on success.
        :param user_id:
        :param png_sticker:
        :return:
        """
        result = apihelper.upload_sticker_file(self.token, user_id, png_sticker)
        return types.File.de_json(result)

    def create_new_sticker_set(self, user_id, name, title, png_sticker, emojis, contains_masks=None, mask_position=None):
        """
        Use this method to create new sticker set owned by a user. The bot will be able to edit the created sticker set.
        Returns True on success.
        :param user_id:
        :param name:
        :param title:
        :param png_sticker:
        :param emojis:
        :param contains_masks:
        :param mask_position:
        :return:
        """
        return apihelper.create_new_sticker_set(self.token, user_id, name, title, png_sticker, emojis, contains_masks, mask_position)

    def add_sticker_to_set(self, user_id, name, png_sticker, emojis, mask_position=None):
        """
        Use this method to add a new sticker to a set created by the bot. Returns True on success.
        :param user_id:
        :param name:
        :param png_sticker:
        :param emojis:
        :param mask_position:
        :return:
        """
        return apihelper.add_sticker_to_set(self.token, user_id, name, png_sticker, emojis, mask_position)

    def set_sticker_position_in_set(self, sticker, position):
        """
        Use this method to move a sticker in a set created by the bot to a specific position . Returns True on success.
        :param sticker:
        :param position:
        :return:
        """
        return apihelper.set_sticker_position_in_set(self.token, sticker, position)

    def delete_sticker_from_set(self, sticker):
        """
        Use this method to delete a sticker from a set created by the bot. Returns True on success.
        :param sticker:
        :return:
        """
        return apihelper.delete_sticker_from_set(self.token, sticker)

    def register_for_reply--- This code section failed: ---

 L.1655         0  LOAD_FAST                'message'
                2  LOAD_ATTR                message_id
                4  STORE_FAST               'message_id'

 L.1656         6  LOAD_FAST                'self'
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

 L.1668         0  LOAD_FAST                'self'
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

 L.1676         0  LOAD_FAST                'new_messages'
                2  GET_ITER         
              4_0  COME_FROM            46  '46'
              4_1  COME_FROM            26  '26'
              4_2  COME_FROM            16  '16'
                4  FOR_ITER             98  'to 98'
                6  STORE_FAST               'message'

 L.1677         8  LOAD_GLOBAL              hasattr
               10  LOAD_FAST                'message'
               12  LOAD_STR                 'reply_to_message'
               14  CALL_FUNCTION_2       2  ''
               16  POP_JUMP_IF_FALSE     4  'to 4'
               18  LOAD_FAST                'message'
               20  LOAD_ATTR                reply_to_message
               22  LOAD_CONST               None
               24  <117>                 1  ''
               26  POP_JUMP_IF_FALSE     4  'to 4'

 L.1678        28  LOAD_FAST                'self'
               30  LOAD_ATTR                reply_backend
               32  LOAD_METHOD              get_handlers
               34  LOAD_FAST                'message'
               36  LOAD_ATTR                reply_to_message
               38  LOAD_ATTR                message_id
               40  CALL_METHOD_1         1  ''
               42  STORE_FAST               'handlers'

 L.1679        44  LOAD_FAST                'handlers'
               46  POP_JUMP_IF_FALSE     4  'to 4'

 L.1680        48  LOAD_FAST                'handlers'
               50  GET_ITER         
               52  FOR_ITER             96  'to 96'
               54  STORE_FAST               'handler'

 L.1681        56  LOAD_FAST                'self'
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
               96  JUMP_BACK             4  'to 4'

Parse error at or near `<117>' instruction at offset 24

    def register_next_step_handler--- This code section failed: ---

 L.1694         0  LOAD_FAST                'message'
                2  LOAD_ATTR                chat
                4  LOAD_ATTR                id
                6  STORE_FAST               'chat_id'

 L.1695         8  LOAD_FAST                'self'
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

 L.1708         0  LOAD_FAST                'self'
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

    def clear_step_handler(self, message):
        """
        Clears all callback functions registered by register_next_step_handler().

        :param message:     The message for which we want to handle new message after that in same chat.
        """
        chat_id = message.chat.id
        self.clear_step_handler_by_chat_id(chat_id)

    def clear_step_handler_by_chat_id(self, chat_id):
        """
        Clears all callback functions registered by register_next_step_handler().

        :param chat_id: The chat for which we want to clear next step handlers
        """
        self.next_step_backend.clear_handlers(chat_id)

    def clear_reply_handlers(self, message):
        """
        Clears all callback functions registered by register_for_reply() and register_for_reply_by_message_id().

        :param message: The message for which we want to clear reply handlers
        """
        message_id = message.message_id
        self.clear_reply_handlers_by_message_id(message_id)

    def clear_reply_handlers_by_message_id(self, message_id):
        """
        Clears all callback functions registered by register_for_reply() and register_for_reply_by_message_id().

        :param message_id: The message id for which we want to clear reply handlers
        """
        self.reply_backend.clear_handlers(message_id)

    def _notify_next_handlers--- This code section failed: ---

 L.1750         0  LOAD_GLOBAL              enumerate
                2  LOAD_FAST                'new_messages'
                4  CALL_FUNCTION_1       1  ''
                6  GET_ITER         
              8_0  COME_FROM            94  '94'
                8  FOR_ITER            108  'to 108'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'i'
               14  STORE_FAST               'message'

 L.1751        16  LOAD_CONST               False
               18  STORE_FAST               'need_pop'

 L.1752        20  LOAD_FAST                'self'
               22  LOAD_ATTR                next_step_backend
               24  LOAD_METHOD              get_handlers
               26  LOAD_FAST                'message'
               28  LOAD_ATTR                chat
               30  LOAD_ATTR                id
               32  CALL_METHOD_1         1  ''
               34  STORE_FAST               'handlers'

 L.1753        36  LOAD_FAST                'handlers'
               38  POP_JUMP_IF_FALSE    92  'to 92'

 L.1754        40  LOAD_FAST                'handlers'
               42  GET_ITER         
               44  FOR_ITER             92  'to 92'
               46  STORE_FAST               'handler'

 L.1755        48  LOAD_CONST               True
               50  STORE_FAST               'need_pop'

 L.1756        52  LOAD_FAST                'self'
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
             92_0  COME_FROM            38  '38'

 L.1757        92  LOAD_FAST                'need_pop'
               94  POP_JUMP_IF_FALSE     8  'to 8'

 L.1758        96  LOAD_FAST                'new_messages'
               98  LOAD_METHOD              pop
              100  LOAD_FAST                'i'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          
              106  JUMP_BACK             8  'to 8'

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
        elif update_types:
            for update_type in update_types:
                self.typed_middleware_handlers[update_type].append(handler)

        else:
            self.default_middleware_handlers.append(handler)

    def message_handler--- This code section failed: ---

 L.1852         0  LOAD_DEREF               'content_types'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.1853         8  LOAD_STR                 'text'
               10  BUILD_LIST_1          1 
               12  STORE_DEREF              'content_types'
             14_0  COME_FROM             6  '6'

 L.1855        14  LOAD_CLOSURE             'commands'
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

 L.1865        36  LOAD_FAST                'decorator'
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

 L.1886         0  LOAD_DEREF               'content_types'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.1887         8  LOAD_STR                 'text'
               10  BUILD_LIST_1          1 
               12  STORE_DEREF              'content_types'
             14_0  COME_FROM             6  '6'

 L.1889        14  LOAD_CLOSURE             'commands'
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

 L.1899        36  LOAD_FAST                'decorator'
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

 L.1920         0  LOAD_DEREF               'content_types'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.1921         8  LOAD_STR                 'text'
               10  BUILD_LIST_1          1 
               12  STORE_DEREF              'content_types'
             14_0  COME_FROM             6  '6'

 L.1923        14  LOAD_CLOSURE             'commands'
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

 L.1933        36  LOAD_FAST                'decorator'
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

 L.1954         0  LOAD_DEREF               'content_types'
                2  LOAD_CONST               None
                4  <117>                 0  ''
                6  POP_JUMP_IF_FALSE    14  'to 14'

 L.1955         8  LOAD_STR                 'text'
               10  BUILD_LIST_1          1 
               12  STORE_DEREF              'content_types'
             14_0  COME_FROM             6  '6'

 L.1957        14  LOAD_CLOSURE             'commands'
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

 L.1967        36  LOAD_FAST                'decorator'
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

 L.1986         0  LOAD_DEREF               'self'
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

 L.1987        22  LOAD_DEREF               'self'
               24  LOAD_METHOD              add_inline_handler
               26  LOAD_FAST                'handler_dict'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.1988        32  LOAD_FAST                'handler'
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

 L.2009         0  LOAD_DEREF               'self'
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

 L.2010        22  LOAD_DEREF               'self'
               24  LOAD_METHOD              add_chosen_inline_handler
               26  LOAD_FAST                'handler_dict'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.2011        32  LOAD_FAST                'handler'
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

 L.2032         0  LOAD_DEREF               'self'
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

 L.2033        22  LOAD_DEREF               'self'
               24  LOAD_METHOD              add_callback_query_handler
               26  LOAD_FAST                'handler_dict'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.2034        32  LOAD_FAST                'handler'
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

 L.2055         0  LOAD_DEREF               'self'
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

 L.2056        22  LOAD_DEREF               'self'
               24  LOAD_METHOD              add_shipping_query_handler
               26  LOAD_FAST                'handler_dict'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.2057        32  LOAD_FAST                'handler'
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

 L.2078         0  LOAD_DEREF               'self'
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

 L.2079        22  LOAD_DEREF               'self'
               24  LOAD_METHOD              add_pre_checkout_query_handler
               26  LOAD_FAST                'handler_dict'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.2080        32  LOAD_FAST                'handler'
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

 L.2101         0  LOAD_DEREF               'self'
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

 L.2102        22  LOAD_DEREF               'self'
               24  LOAD_METHOD              add_poll_handler
               26  LOAD_FAST                'handler_dict'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.2103        32  LOAD_FAST                'handler'
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

 L.2124         0  LOAD_DEREF               'self'
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

 L.2125        22  LOAD_DEREF               'self'
               24  LOAD_METHOD              add_poll_answer_handler
               26  LOAD_FAST                'handler_dict'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.2126        32  LOAD_FAST                'handler'
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

    def _test_message_handler--- This code section failed: ---

 L.2145         0  LOAD_FAST                'message_handler'
                2  LOAD_STR                 'filters'
                4  BINARY_SUBSCR    
                6  LOAD_METHOD              items
                8  CALL_METHOD_0         0  ''
               10  GET_ITER         
             12_0  COME_FROM            42  '42'
               12  FOR_ITER             52  'to 52'
               14  UNPACK_SEQUENCE_2     2 
               16  STORE_FAST               'message_filter'
               18  STORE_FAST               'filter_value'

 L.2146        20  LOAD_FAST                'filter_value'
               22  LOAD_CONST               None
               24  <117>                 0  ''
               26  POP_JUMP_IF_FALSE    30  'to 30'

 L.2147        28  JUMP_BACK            12  'to 12'
             30_0  COME_FROM            26  '26'

 L.2149        30  LOAD_FAST                'self'
               32  LOAD_METHOD              _test_filter
               34  LOAD_FAST                'message_filter'
               36  LOAD_FAST                'filter_value'
               38  LOAD_FAST                'message'
               40  CALL_METHOD_3         3  ''
               42  POP_JUMP_IF_TRUE     12  'to 12'

 L.2150        44  POP_TOP          
               46  LOAD_CONST               False
               48  RETURN_VALUE     
               50  JUMP_BACK            12  'to 12'

 L.2152        52  LOAD_CONST               True
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

 L.2164         0  LOAD_FAST                'msg'
                2  LOAD_ATTR                content_type
                4  LOAD_DEREF               'filter_value'
                6  <118>                 0  ''
                8  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
,  'regexp':lambda msg: msg.content_type == 'text' and re.search(filter_value, msg.text, re.IGNORECASE), 
         'commands':--- This code section failed: ---

 L.2166         0  LOAD_FAST                'msg'
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

    def _notify_command_handlers--- This code section failed: ---

 L.2179         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'handlers'
                4  CALL_FUNCTION_1       1  ''
                6  LOAD_CONST               0
                8  COMPARE_OP               ==
               10  POP_JUMP_IF_FALSE    16  'to 16'

 L.2180        12  LOAD_CONST               None
               14  RETURN_VALUE     
             16_0  COME_FROM            10  '10'

 L.2181        16  LOAD_FAST                'new_messages'
               18  GET_ITER         
               20  FOR_ITER             68  'to 68'
               22  STORE_FAST               'message'

 L.2182        24  LOAD_FAST                'handlers'
               26  GET_ITER         
             28_0  COME_FROM            42  '42'
               28  FOR_ITER             66  'to 66'
               30  STORE_FAST               'message_handler'

 L.2183        32  LOAD_FAST                'self'
               34  LOAD_METHOD              _test_message_handler
               36  LOAD_FAST                'message_handler'
               38  LOAD_FAST                'message'
               40  CALL_METHOD_2         2  ''
               42  POP_JUMP_IF_FALSE    28  'to 28'

 L.2184        44  LOAD_FAST                'self'
               46  LOAD_METHOD              _exec_task
               48  LOAD_FAST                'message_handler'
               50  LOAD_STR                 'function'
               52  BINARY_SUBSCR    
               54  LOAD_FAST                'message'
               56  CALL_METHOD_2         2  ''
               58  POP_TOP          

 L.2185        60  POP_TOP          
               62  CONTINUE             20  'to 20'
               64  JUMP_BACK            28  'to 28'
               66  JUMP_BACK            20  'to 20'

Parse error at or near `CONTINUE' instruction at offset 62


class AsyncTeleBot(TeleBot):

    def __init__--- This code section failed: ---

 L.2190         0  LOAD_GLOBAL              TeleBot
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
    def get_file--- This code section failed: ---

 L.2222         0  LOAD_GLOBAL              TeleBot
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

 L.2226         0  LOAD_GLOBAL              TeleBot
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

 L.2230         0  LOAD_GLOBAL              TeleBot
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

 L.2234         0  LOAD_GLOBAL              TeleBot
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

 L.2238         0  LOAD_GLOBAL              TeleBot
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

 L.2242         0  LOAD_GLOBAL              TeleBot
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

 L.2246         0  LOAD_GLOBAL              TeleBot
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

 L.2250         0  LOAD_GLOBAL              TeleBot
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

 L.2254         0  LOAD_GLOBAL              TeleBot
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

 L.2258         0  LOAD_GLOBAL              TeleBot
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

 L.2262         0  LOAD_GLOBAL              TeleBot
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

 L.2266         0  LOAD_GLOBAL              TeleBot
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
    def forward_message--- This code section failed: ---

 L.2270         0  LOAD_GLOBAL              TeleBot
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
    def delete_message--- This code section failed: ---

 L.2274         0  LOAD_GLOBAL              TeleBot
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

 L.2278         0  LOAD_GLOBAL              TeleBot
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

 L.2282         0  LOAD_GLOBAL              TeleBot
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

 L.2286         0  LOAD_GLOBAL              TeleBot
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

 L.2290         0  LOAD_GLOBAL              TeleBot
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

 L.2294         0  LOAD_GLOBAL              TeleBot
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

 L.2298         0  LOAD_GLOBAL              TeleBot
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

 L.2302         0  LOAD_GLOBAL              TeleBot
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

 L.2306         0  LOAD_GLOBAL              TeleBot
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

 L.2310         0  LOAD_GLOBAL              TeleBot
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

 L.2314         0  LOAD_GLOBAL              TeleBot
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

 L.2318         0  LOAD_GLOBAL              TeleBot
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

 L.2322         0  LOAD_GLOBAL              TeleBot
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

 L.2326         0  LOAD_GLOBAL              TeleBot
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

 L.2330         0  LOAD_GLOBAL              TeleBot
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

 L.2334         0  LOAD_GLOBAL              TeleBot
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

 L.2338         0  LOAD_GLOBAL              TeleBot
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

 L.2342         0  LOAD_GLOBAL              TeleBot
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

 L.2346         0  LOAD_GLOBAL              TeleBot
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
    def export_chat_invite_link--- This code section failed: ---

 L.2350         0  LOAD_GLOBAL              TeleBot
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

 L.2354         0  LOAD_GLOBAL              TeleBot
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

 L.2358         0  LOAD_GLOBAL              TeleBot
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

 L.2362         0  LOAD_GLOBAL              TeleBot
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

 L.2366         0  LOAD_GLOBAL              TeleBot
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

 L.2370         0  LOAD_GLOBAL              TeleBot
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

 L.2374         0  LOAD_GLOBAL              TeleBot
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

 L.2378         0  LOAD_GLOBAL              TeleBot
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

 L.2382         0  LOAD_GLOBAL              TeleBot
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

 L.2386         0  LOAD_GLOBAL              TeleBot
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

 L.2390         0  LOAD_GLOBAL              TeleBot
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

 L.2394         0  LOAD_GLOBAL              TeleBot
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

 L.2398         0  LOAD_GLOBAL              TeleBot
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

 L.2402         0  LOAD_GLOBAL              TeleBot
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

 L.2406         0  LOAD_GLOBAL              TeleBot
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

 L.2410         0  LOAD_GLOBAL              TeleBot
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

 L.2414         0  LOAD_GLOBAL              TeleBot
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

 L.2418         0  LOAD_GLOBAL              TeleBot
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

 L.2422         0  LOAD_GLOBAL              TeleBot
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

 L.2426         0  LOAD_GLOBAL              TeleBot
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

 L.2430         0  LOAD_GLOBAL              TeleBot
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

 L.2434         0  LOAD_GLOBAL              TeleBot
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

 L.2438         0  LOAD_GLOBAL              TeleBot
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

 L.2442         0  LOAD_GLOBAL              TeleBot
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

 L.2446         0  LOAD_GLOBAL              TeleBot
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

 L.2450         0  LOAD_GLOBAL              TeleBot
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
    def send_poll--- This code section failed: ---

 L.2454         0  LOAD_GLOBAL              TeleBot
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

 L.2458         0  LOAD_GLOBAL              TeleBot
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