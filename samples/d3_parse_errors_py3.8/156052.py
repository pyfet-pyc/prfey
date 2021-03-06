# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
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
        :param allowed_updates: A JSON-serialized list of the update types you want your bot to receive. For example, specify [???message???, ???edited_channel_post???, ???callback_query???] to only receive updates of these types. See Update for a complete list of available update types. Specify an empty list to receive all updates regardless of type (default). If not specified, the previous setting will be used.
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
        while True:
            if updates:
                total += len(updates)
                for update in updates:
                    if update.update_id > self.last_update_id:
                        self.last_update_id = update.update_id
                else:
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

 L. 328         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'updates'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'upd_count'

 L. 329         8  LOAD_GLOBAL              logger
               10  LOAD_METHOD              debug
               12  LOAD_STR                 'Received {0} new updates'
               14  LOAD_METHOD              format
               16  LOAD_FAST                'upd_count'
               18  CALL_METHOD_1         1  ''
               20  CALL_METHOD_1         1  ''
               22  POP_TOP          

 L. 330        24  LOAD_FAST                'upd_count'
               26  LOAD_CONST               0
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    36  'to 36'

 L. 331        32  LOAD_CONST               None
               34  RETURN_VALUE     
             36_0  COME_FROM            30  '30'

 L. 333        36  LOAD_CONST               None
               38  STORE_FAST               'new_messages'

 L. 334        40  LOAD_CONST               None
               42  STORE_FAST               'new_edited_messages'

 L. 335        44  LOAD_CONST               None
               46  STORE_FAST               'new_channel_posts'

 L. 336        48  LOAD_CONST               None
               50  STORE_FAST               'new_edited_channel_posts'

 L. 337        52  LOAD_CONST               None
               54  STORE_FAST               'new_inline_queries'

 L. 338        56  LOAD_CONST               None
               58  STORE_FAST               'new_chosen_inline_results'

 L. 339        60  LOAD_CONST               None
               62  STORE_FAST               'new_callback_queries'

 L. 340        64  LOAD_CONST               None
               66  STORE_FAST               'new_shipping_queries'

 L. 341        68  LOAD_CONST               None
               70  STORE_FAST               'new_pre_checkout_queries'

 L. 342        72  LOAD_CONST               None
               74  STORE_FAST               'new_polls'

 L. 343        76  LOAD_CONST               None
               78  STORE_FAST               'new_poll_answers'

 L. 345        80  LOAD_FAST                'updates'
               82  GET_ITER         
             84_0  COME_FROM           586  '586'
             84_1  COME_FROM           558  '558'
             84_2  COME_FROM           178  '178'
            84_86  FOR_ITER            588  'to 588'
               88  STORE_FAST               'update'

 L. 346        90  LOAD_GLOBAL              apihelper
               92  LOAD_ATTR                ENABLE_MIDDLEWARE
               94  POP_JUMP_IF_FALSE   198  'to 198'

 L. 347        96  SETUP_FINALLY       112  'to 112'

 L. 348        98  LOAD_FAST                'self'
              100  LOAD_METHOD              process_middlewares
              102  LOAD_FAST                'update'
              104  CALL_METHOD_1         1  ''
              106  POP_TOP          
              108  POP_BLOCK        
              110  JUMP_FORWARD        198  'to 198'
            112_0  COME_FROM_FINALLY    96  '96'

 L. 349       112  DUP_TOP          
              114  LOAD_GLOBAL              Exception
              116  COMPARE_OP               exception-match
              118  POP_JUMP_IF_FALSE   196  'to 196'
              120  POP_TOP          
              122  STORE_FAST               'e'
              124  POP_TOP          
              126  SETUP_FINALLY       184  'to 184'

 L. 350       128  LOAD_GLOBAL              logger
              130  LOAD_METHOD              error
              132  LOAD_GLOBAL              str
              134  LOAD_FAST                'e'
              136  CALL_FUNCTION_1       1  ''
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          

 L. 351       142  LOAD_FAST                'self'
              144  LOAD_ATTR                suppress_middleware_excepions
              146  POP_JUMP_IF_TRUE    152  'to 152'

 L. 352       148  RAISE_VARARGS_0       0  'reraise'
              150  JUMP_FORWARD        180  'to 180'
            152_0  COME_FROM           146  '146'

 L. 354       152  LOAD_FAST                'update'
              154  LOAD_ATTR                update_id
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                last_update_id
              160  COMPARE_OP               >
              162  POP_JUMP_IF_FALSE   172  'to 172'

 L. 354       164  LOAD_FAST                'update'
              166  LOAD_ATTR                update_id
              168  LOAD_FAST                'self'
              170  STORE_ATTR               last_update_id
            172_0  COME_FROM           162  '162'

 L. 355       172  POP_BLOCK        
              174  POP_EXCEPT       
              176  CALL_FINALLY        184  'to 184'
              178  JUMP_BACK            84  'to 84'
            180_0  COME_FROM           150  '150'
              180  POP_BLOCK        
              182  BEGIN_FINALLY    
            184_0  COME_FROM           176  '176'
            184_1  COME_FROM_FINALLY   126  '126'
              184  LOAD_CONST               None
              186  STORE_FAST               'e'
              188  DELETE_FAST              'e'
              190  END_FINALLY      
              192  POP_EXCEPT       
              194  JUMP_FORWARD        198  'to 198'
            196_0  COME_FROM           118  '118'
              196  END_FINALLY      
            198_0  COME_FROM           194  '194'
            198_1  COME_FROM           110  '110'
            198_2  COME_FROM            94  '94'

 L. 357       198  LOAD_FAST                'update'
              200  LOAD_ATTR                update_id
              202  LOAD_FAST                'self'
              204  LOAD_ATTR                last_update_id
              206  COMPARE_OP               >
              208  POP_JUMP_IF_FALSE   218  'to 218'

 L. 358       210  LOAD_FAST                'update'
              212  LOAD_ATTR                update_id
              214  LOAD_FAST                'self'
              216  STORE_ATTR               last_update_id
            218_0  COME_FROM           208  '208'

 L. 359       218  LOAD_FAST                'update'
              220  LOAD_ATTR                message
              222  POP_JUMP_IF_FALSE   248  'to 248'

 L. 360       224  LOAD_FAST                'new_messages'
              226  LOAD_CONST               None
              228  COMPARE_OP               is
              230  POP_JUMP_IF_FALSE   236  'to 236'

 L. 360       232  BUILD_LIST_0          0 
              234  STORE_FAST               'new_messages'
            236_0  COME_FROM           230  '230'

 L. 361       236  LOAD_FAST                'new_messages'
              238  LOAD_METHOD              append
              240  LOAD_FAST                'update'
              242  LOAD_ATTR                message
              244  CALL_METHOD_1         1  ''
              246  POP_TOP          
            248_0  COME_FROM           222  '222'

 L. 362       248  LOAD_FAST                'update'
              250  LOAD_ATTR                edited_message
          252_254  POP_JUMP_IF_FALSE   282  'to 282'

 L. 363       256  LOAD_FAST                'new_edited_messages'
              258  LOAD_CONST               None
              260  COMPARE_OP               is
          262_264  POP_JUMP_IF_FALSE   270  'to 270'

 L. 363       266  BUILD_LIST_0          0 
              268  STORE_FAST               'new_edited_messages'
            270_0  COME_FROM           262  '262'

 L. 364       270  LOAD_FAST                'new_edited_messages'
              272  LOAD_METHOD              append
              274  LOAD_FAST                'update'
              276  LOAD_ATTR                edited_message
              278  CALL_METHOD_1         1  ''
              280  POP_TOP          
            282_0  COME_FROM           252  '252'

 L. 365       282  LOAD_FAST                'update'
              284  LOAD_ATTR                channel_post
          286_288  POP_JUMP_IF_FALSE   316  'to 316'

 L. 366       290  LOAD_FAST                'new_channel_posts'
              292  LOAD_CONST               None
              294  COMPARE_OP               is
          296_298  POP_JUMP_IF_FALSE   304  'to 304'

 L. 366       300  BUILD_LIST_0          0 
              302  STORE_FAST               'new_channel_posts'
            304_0  COME_FROM           296  '296'

 L. 367       304  LOAD_FAST                'new_channel_posts'
              306  LOAD_METHOD              append
              308  LOAD_FAST                'update'
              310  LOAD_ATTR                channel_post
              312  CALL_METHOD_1         1  ''
              314  POP_TOP          
            316_0  COME_FROM           286  '286'

 L. 368       316  LOAD_FAST                'update'
              318  LOAD_ATTR                edited_channel_post
          320_322  POP_JUMP_IF_FALSE   350  'to 350'

 L. 369       324  LOAD_FAST                'new_edited_channel_posts'
              326  LOAD_CONST               None
              328  COMPARE_OP               is
          330_332  POP_JUMP_IF_FALSE   338  'to 338'

 L. 369       334  BUILD_LIST_0          0 
              336  STORE_FAST               'new_edited_channel_posts'
            338_0  COME_FROM           330  '330'

 L. 370       338  LOAD_FAST                'new_edited_channel_posts'
              340  LOAD_METHOD              append
              342  LOAD_FAST                'update'
              344  LOAD_ATTR                edited_channel_post
              346  CALL_METHOD_1         1  ''
              348  POP_TOP          
            350_0  COME_FROM           320  '320'

 L. 371       350  LOAD_FAST                'update'
              352  LOAD_ATTR                inline_query
          354_356  POP_JUMP_IF_FALSE   384  'to 384'

 L. 372       358  LOAD_FAST                'new_inline_queries'
              360  LOAD_CONST               None
              362  COMPARE_OP               is
          364_366  POP_JUMP_IF_FALSE   372  'to 372'

 L. 372       368  BUILD_LIST_0          0 
              370  STORE_FAST               'new_inline_queries'
            372_0  COME_FROM           364  '364'

 L. 373       372  LOAD_FAST                'new_inline_queries'
              374  LOAD_METHOD              append
              376  LOAD_FAST                'update'
              378  LOAD_ATTR                inline_query
              380  CALL_METHOD_1         1  ''
              382  POP_TOP          
            384_0  COME_FROM           354  '354'

 L. 374       384  LOAD_FAST                'update'
              386  LOAD_ATTR                chosen_inline_result
          388_390  POP_JUMP_IF_FALSE   418  'to 418'

 L. 375       392  LOAD_FAST                'new_chosen_inline_results'
              394  LOAD_CONST               None
              396  COMPARE_OP               is
          398_400  POP_JUMP_IF_FALSE   406  'to 406'

 L. 375       402  BUILD_LIST_0          0 
              404  STORE_FAST               'new_chosen_inline_results'
            406_0  COME_FROM           398  '398'

 L. 376       406  LOAD_FAST                'new_chosen_inline_results'
              408  LOAD_METHOD              append
              410  LOAD_FAST                'update'
              412  LOAD_ATTR                chosen_inline_result
              414  CALL_METHOD_1         1  ''
              416  POP_TOP          
            418_0  COME_FROM           388  '388'

 L. 377       418  LOAD_FAST                'update'
              420  LOAD_ATTR                callback_query
          422_424  POP_JUMP_IF_FALSE   452  'to 452'

 L. 378       426  LOAD_FAST                'new_callback_queries'
              428  LOAD_CONST               None
              430  COMPARE_OP               is
          432_434  POP_JUMP_IF_FALSE   440  'to 440'

 L. 378       436  BUILD_LIST_0          0 
              438  STORE_FAST               'new_callback_queries'
            440_0  COME_FROM           432  '432'

 L. 379       440  LOAD_FAST                'new_callback_queries'
              442  LOAD_METHOD              append
              444  LOAD_FAST                'update'
              446  LOAD_ATTR                callback_query
              448  CALL_METHOD_1         1  ''
              450  POP_TOP          
            452_0  COME_FROM           422  '422'

 L. 380       452  LOAD_FAST                'update'
              454  LOAD_ATTR                shipping_query
          456_458  POP_JUMP_IF_FALSE   486  'to 486'

 L. 381       460  LOAD_FAST                'new_shipping_queries'
              462  LOAD_CONST               None
              464  COMPARE_OP               is
          466_468  POP_JUMP_IF_FALSE   474  'to 474'

 L. 381       470  BUILD_LIST_0          0 
              472  STORE_FAST               'new_shipping_queries'
            474_0  COME_FROM           466  '466'

 L. 382       474  LOAD_FAST                'new_shipping_queries'
              476  LOAD_METHOD              append
              478  LOAD_FAST                'update'
              480  LOAD_ATTR                shipping_query
              482  CALL_METHOD_1         1  ''
              484  POP_TOP          
            486_0  COME_FROM           456  '456'

 L. 383       486  LOAD_FAST                'update'
              488  LOAD_ATTR                pre_checkout_query
          490_492  POP_JUMP_IF_FALSE   520  'to 520'

 L. 384       494  LOAD_FAST                'new_pre_checkout_queries'
              496  LOAD_CONST               None
              498  COMPARE_OP               is
          500_502  POP_JUMP_IF_FALSE   508  'to 508'

 L. 384       504  BUILD_LIST_0          0 
              506  STORE_FAST               'new_pre_checkout_queries'
            508_0  COME_FROM           500  '500'

 L. 385       508  LOAD_FAST                'new_pre_checkout_queries'
              510  LOAD_METHOD              append
              512  LOAD_FAST                'update'
              514  LOAD_ATTR                pre_checkout_query
              516  CALL_METHOD_1         1  ''
              518  POP_TOP          
            520_0  COME_FROM           490  '490'

 L. 386       520  LOAD_FAST                'update'
              522  LOAD_ATTR                poll
          524_526  POP_JUMP_IF_FALSE   554  'to 554'

 L. 387       528  LOAD_FAST                'new_polls'
              530  LOAD_CONST               None
              532  COMPARE_OP               is
          534_536  POP_JUMP_IF_FALSE   542  'to 542'

 L. 387       538  BUILD_LIST_0          0 
              540  STORE_FAST               'new_polls'
            542_0  COME_FROM           534  '534'

 L. 388       542  LOAD_FAST                'new_polls'
              544  LOAD_METHOD              append
              546  LOAD_FAST                'update'
              548  LOAD_ATTR                poll
              550  CALL_METHOD_1         1  ''
              552  POP_TOP          
            554_0  COME_FROM           524  '524'

 L. 389       554  LOAD_FAST                'update'
              556  LOAD_ATTR                poll_answer
              558  POP_JUMP_IF_FALSE_BACK    84  'to 84'

 L. 390       560  LOAD_FAST                'new_poll_answers'
              562  LOAD_CONST               None
              564  COMPARE_OP               is
          566_568  POP_JUMP_IF_FALSE   574  'to 574'

 L. 390       570  BUILD_LIST_0          0 
              572  STORE_FAST               'new_poll_answers'
            574_0  COME_FROM           566  '566'

 L. 391       574  LOAD_FAST                'new_poll_answers'
              576  LOAD_METHOD              append
              578  LOAD_FAST                'update'
              580  LOAD_ATTR                poll_answer
              582  CALL_METHOD_1         1  ''
              584  POP_TOP          
              586  JUMP_BACK            84  'to 84'
            588_0  COME_FROM            84  '84'

 L. 393       588  LOAD_FAST                'new_messages'
          590_592  POP_JUMP_IF_FALSE   604  'to 604'

 L. 394       594  LOAD_FAST                'self'
              596  LOAD_METHOD              process_new_messages
              598  LOAD_FAST                'new_messages'
              600  CALL_METHOD_1         1  ''
              602  POP_TOP          
            604_0  COME_FROM           590  '590'

 L. 395       604  LOAD_FAST                'new_edited_messages'
          606_608  POP_JUMP_IF_FALSE   620  'to 620'

 L. 396       610  LOAD_FAST                'self'
              612  LOAD_METHOD              process_new_edited_messages
              614  LOAD_FAST                'new_edited_messages'
              616  CALL_METHOD_1         1  ''
              618  POP_TOP          
            620_0  COME_FROM           606  '606'

 L. 397       620  LOAD_FAST                'new_channel_posts'
          622_624  POP_JUMP_IF_FALSE   636  'to 636'

 L. 398       626  LOAD_FAST                'self'
              628  LOAD_METHOD              process_new_channel_posts
              630  LOAD_FAST                'new_channel_posts'
              632  CALL_METHOD_1         1  ''
              634  POP_TOP          
            636_0  COME_FROM           622  '622'

 L. 399       636  LOAD_FAST                'new_edited_channel_posts'
          638_640  POP_JUMP_IF_FALSE   652  'to 652'

 L. 400       642  LOAD_FAST                'self'
              644  LOAD_METHOD              process_new_edited_channel_posts
              646  LOAD_FAST                'new_edited_channel_posts'
              648  CALL_METHOD_1         1  ''
              650  POP_TOP          
            652_0  COME_FROM           638  '638'

 L. 401       652  LOAD_FAST                'new_inline_queries'
          654_656  POP_JUMP_IF_FALSE   668  'to 668'

 L. 402       658  LOAD_FAST                'self'
              660  LOAD_METHOD              process_new_inline_query
              662  LOAD_FAST                'new_inline_queries'
              664  CALL_METHOD_1         1  ''
              666  POP_TOP          
            668_0  COME_FROM           654  '654'

 L. 403       668  LOAD_FAST                'new_chosen_inline_results'
          670_672  POP_JUMP_IF_FALSE   684  'to 684'

 L. 404       674  LOAD_FAST                'self'
              676  LOAD_METHOD              process_new_chosen_inline_query
              678  LOAD_FAST                'new_chosen_inline_results'
              680  CALL_METHOD_1         1  ''
              682  POP_TOP          
            684_0  COME_FROM           670  '670'

 L. 405       684  LOAD_FAST                'new_callback_queries'
          686_688  POP_JUMP_IF_FALSE   700  'to 700'

 L. 406       690  LOAD_FAST                'self'
              692  LOAD_METHOD              process_new_callback_query
              694  LOAD_FAST                'new_callback_queries'
              696  CALL_METHOD_1         1  ''
              698  POP_TOP          
            700_0  COME_FROM           686  '686'

 L. 407       700  LOAD_FAST                'new_shipping_queries'
          702_704  POP_JUMP_IF_FALSE   716  'to 716'

 L. 408       706  LOAD_FAST                'self'
              708  LOAD_METHOD              process_new_shipping_query
              710  LOAD_FAST                'new_shipping_queries'
              712  CALL_METHOD_1         1  ''
              714  POP_TOP          
            716_0  COME_FROM           702  '702'

 L. 409       716  LOAD_FAST                'new_pre_checkout_queries'
          718_720  POP_JUMP_IF_FALSE   732  'to 732'

 L. 410       722  LOAD_FAST                'self'
              724  LOAD_METHOD              process_new_pre_checkout_query
              726  LOAD_FAST                'new_pre_checkout_queries'
              728  CALL_METHOD_1         1  ''
              730  POP_TOP          
            732_0  COME_FROM           718  '718'

 L. 411       732  LOAD_FAST                'new_polls'
          734_736  POP_JUMP_IF_FALSE   748  'to 748'

 L. 412       738  LOAD_FAST                'self'
              740  LOAD_METHOD              process_new_poll
              742  LOAD_FAST                'new_polls'
              744  CALL_METHOD_1         1  ''
              746  POP_TOP          
            748_0  COME_FROM           734  '734'

 L. 413       748  LOAD_FAST                'new_poll_answers'
          750_752  POP_JUMP_IF_FALSE   764  'to 764'

 L. 414       754  LOAD_FAST                'self'
              756  LOAD_METHOD              process_new_poll_answer
              758  LOAD_FAST                'new_poll_answers'
              760  CALL_METHOD_1         1  ''
              762  POP_TOP          
            764_0  COME_FROM           750  '750'

Parse error at or near `CALL_FINALLY' instruction at offset 176

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

    def process_middlewares(self, update):
        for update_type, middlewares in self.typed_middleware_handlers.items():
            if getattr(update, update_type) is not None:
                for typed_middleware_handler in middlewares:
                    try:
                        typed_middleware_handler(self, getattr(update, update_type))
                    except Exception as e:
                        try:
                            e.args = e.args + (f'Typed middleware handler "{typed_middleware_handler.__qualname__}"',)
                            raise
                        finally:
                            e = None
                            del e

        else:
            if len(self.default_middleware_handlers) > 0:
                for default_middleware_handler in self.default_middleware_handlers:
                    try:
                        default_middleware_handler(self, update)
                    except Exception as e:
                        try:
                            e.args = e.args + (f'Default middleware handler "{default_middleware_handler.__qualname__}"',)
                            raise
                        finally:
                            e = None
                            del e

    def __notify_update(self, new_messages):
        if len(self.update_listener) == 0:
            return
        for listener in self.update_listener:
            self._exec_task(listener, new_messages)

    def infinity_polling--- This code section failed: ---
              0_0  COME_FROM           176  '176'
              0_1  COME_FROM           164  '164'
              0_2  COME_FROM           154  '154'
              0_3  COME_FROM           132  '132'

 L. 484         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _TeleBot__stop_polling
                4  LOAD_METHOD              is_set
                6  CALL_METHOD_0         0  ''
                8  POP_JUMP_IF_TRUE    178  'to 178'

 L. 485        10  SETUP_FINALLY        40  'to 40'

 L. 486        12  LOAD_FAST                'self'
               14  LOAD_ATTR                polling
               16  LOAD_FAST                'args'
               18  LOAD_CONST               True
               20  LOAD_FAST                'timeout'
               22  LOAD_FAST                'long_polling_timeout'
               24  LOAD_CONST               ('none_stop', 'timeout', 'long_polling_timeout')
               26  BUILD_CONST_KEY_MAP_3     3 
               28  LOAD_FAST                'kwargs'
               30  BUILD_MAP_UNPACK_WITH_CALL_2     2 
               32  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               34  POP_TOP          
               36  POP_BLOCK        
               38  JUMP_FORWARD        152  'to 152'
             40_0  COME_FROM_FINALLY    10  '10'

 L. 487        40  DUP_TOP          
               42  LOAD_GLOBAL              Exception
               44  COMPARE_OP               exception-match
               46  POP_JUMP_IF_FALSE   150  'to 150'
               48  POP_TOP          
               50  STORE_FAST               'e'
               52  POP_TOP          
               54  SETUP_FINALLY       138  'to 138'

 L. 488        56  LOAD_FAST                'logger_level'
               58  POP_JUMP_IF_FALSE    86  'to 86'
               60  LOAD_FAST                'logger_level'
               62  LOAD_GLOBAL              logging
               64  LOAD_ATTR                ERROR
               66  COMPARE_OP               >=
               68  POP_JUMP_IF_FALSE    86  'to 86'

 L. 489        70  LOAD_GLOBAL              logger
               72  LOAD_METHOD              error
               74  LOAD_STR                 'Infinity polling exception: %s'
               76  LOAD_GLOBAL              str
               78  LOAD_FAST                'e'
               80  CALL_FUNCTION_1       1  ''
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          
             86_0  COME_FROM            68  '68'
             86_1  COME_FROM            58  '58'

 L. 490        86  LOAD_FAST                'logger_level'
               88  POP_JUMP_IF_FALSE   116  'to 116'
               90  LOAD_FAST                'logger_level'
               92  LOAD_GLOBAL              logging
               94  LOAD_ATTR                DEBUG
               96  COMPARE_OP               >=
               98  POP_JUMP_IF_FALSE   116  'to 116'

 L. 491       100  LOAD_GLOBAL              logger
              102  LOAD_METHOD              error
              104  LOAD_STR                 'Exception traceback:\n%s'
              106  LOAD_GLOBAL              traceback
              108  LOAD_METHOD              format_exc
              110  CALL_METHOD_0         0  ''
              112  CALL_METHOD_2         2  ''
              114  POP_TOP          
            116_0  COME_FROM            98  '98'
            116_1  COME_FROM            88  '88'

 L. 492       116  LOAD_GLOBAL              time
              118  LOAD_METHOD              sleep
              120  LOAD_CONST               3
              122  CALL_METHOD_1         1  ''
              124  POP_TOP          

 L. 493       126  POP_BLOCK        
              128  POP_EXCEPT       
              130  CALL_FINALLY        138  'to 138'
              132  JUMP_BACK             0  'to 0'
              134  POP_BLOCK        
              136  BEGIN_FINALLY    
            138_0  COME_FROM           130  '130'
            138_1  COME_FROM_FINALLY    54  '54'
              138  LOAD_CONST               None
              140  STORE_FAST               'e'
              142  DELETE_FAST              'e'
              144  END_FINALLY      
              146  POP_EXCEPT       
              148  JUMP_FORWARD        152  'to 152'
            150_0  COME_FROM            46  '46'
              150  END_FINALLY      
            152_0  COME_FROM           148  '148'
            152_1  COME_FROM            38  '38'

 L. 494       152  LOAD_FAST                'logger_level'
              154  POP_JUMP_IF_FALSE_BACK     0  'to 0'
              156  LOAD_FAST                'logger_level'
              158  LOAD_GLOBAL              logging
              160  LOAD_ATTR                INFO
              162  COMPARE_OP               >=
              164  POP_JUMP_IF_FALSE_BACK     0  'to 0'

 L. 495       166  LOAD_GLOBAL              logger
              168  LOAD_METHOD              error
              170  LOAD_STR                 'Infinity polling: polling exited'
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          
              176  JUMP_BACK             0  'to 0'
            178_0  COME_FROM             8  '8'

 L. 496       178  LOAD_FAST                'logger_level'
              180  POP_JUMP_IF_FALSE   202  'to 202'
              182  LOAD_FAST                'logger_level'
              184  LOAD_GLOBAL              logging
              186  LOAD_ATTR                INFO
              188  COMPARE_OP               >=
              190  POP_JUMP_IF_FALSE   202  'to 202'

 L. 497       192  LOAD_GLOBAL              logger
              194  LOAD_METHOD              error
              196  LOAD_STR                 'Break infinity polling'
              198  CALL_METHOD_1         1  ''
              200  POP_TOP          
            202_0  COME_FROM           190  '190'
            202_1  COME_FROM           180  '180'

Parse error at or near `CALL_FINALLY' instruction at offset 130

    def polling(self, none_stop=False, interval=0, timeout=20, long_polling_timeout=20):
        """
        This function creates a new Thread that calls an internal __retrieve_updates function.
        This allows the bot to retrieve Updates automagically and notify listeners and message handlers accordingly.

        Warning: Do not call this function more than once!

        Always get updates.
        :param interval: Delay between two update retrivals
        :param none_stop: Do not stop polling when an ApiException occurs.
        :param timeout: Request connection timeout
        :param long_polling_timeout: Timeout in seconds for long polling (see API docs)
        :return:
        """
        if self.threaded:
            self._TeleBot__threaded_polling(none_stop, interval, timeout, long_polling_timeout)
        else:
            self._TeleBot__non_threaded_polling(none_stop, interval, timeout, long_polling_timeout)

    def __threaded_polling(self, non_stop=False, interval=0, timeout=None, long_polling_timeout=None):
        logger.info('Started polling.')
        self._TeleBot__stop_polling.clear()
        error_interval = 0.25
        polling_thread = util.WorkerThread(name='PollingThread')
        or_event = util.OrEvent(polling_thread.done_event, polling_thread.exception_event, self.worker_pool.exception_event)
        while True:
            if not self._TeleBot__stop_polling.wait(interval):
                or_event.clear()
                try:
                    polling_thread.put(self._TeleBot__retrieve_updates, timeout, long_polling_timeout)
                    or_event.wait()
                    polling_thread.raise_exceptions()
                    self.worker_pool.raise_exceptions()
                    error_interval = 0.25
                except apihelper.ApiException as e:
                    try:
                        if self.exception_handler is not None:
                            handled = self.exception_handler.handle(e)
                        else:
                            handled = False
                        if not handled:
                            logger.error(e)
                            if not non_stop:
                                self._TeleBot__stop_polling.set()
                                logger.info('Exception occurred. Stopping.')
                            else:
                                logger.info('Waiting for {0} seconds until retry'.format(error_interval))
                                time.sleep(error_interval)
                                error_interval *= 2
                        else:
                            time.sleep(error_interval)
                        polling_thread.clear_exceptions()
                        self.worker_pool.clear_exceptions()
                    finally:
                        e = None
                        del e

                except KeyboardInterrupt:
                    logger.info('KeyboardInterrupt received.')
                    self._TeleBot__stop_polling.set()
                    break
                except Exception as e:
                    try:
                        if self.exception_handler is not None:
                            handled = self.exception_handler.handle(e)
                        else:
                            handled = False
                        if not handled:
                            polling_thread.stop()
                            polling_thread.clear_exceptions()
                            self.worker_pool.clear_exceptions()
                            raise e
                        else:
                            polling_thread.clear_exceptions()
                            self.worker_pool.clear_exceptions()
                            time.sleep(error_interval)
                    finally:
                        e = None
                        del e

        polling_thread.stop()
        polling_thread.clear_exceptions()
        self.worker_pool.clear_exceptions()
        logger.info('Stopped polling.')

    def __non_threaded_polling(self, non_stop=False, interval=0, timeout=None, long_polling_timeout=None):
        logger.info('Started polling.')
        self._TeleBot__stop_polling.clear()
        error_interval = 0.25
        while True:
            if not self._TeleBot__stop_polling.wait(interval):
                try:
                    self._TeleBot__retrieve_updates(timeout, long_polling_timeout)
                    error_interval = 0.25
                except apihelper.ApiException as e:
                    try:
                        if self.exception_handler is not None:
                            handled = self.exception_handler.handle(e)
                        else:
                            handled = False
                        if not handled:
                            logger.error(e)
                            if not non_stop:
                                self._TeleBot__stop_polling.set()
                                logger.info('Exception occurred. Stopping.')
                            else:
                                logger.info('Waiting for {0} seconds until retry'.format(error_interval))
                                time.sleep(error_interval)
                                error_interval *= 2
                        else:
                            time.sleep(error_interval)
                    finally:
                        e = None
                        del e

                except KeyboardInterrupt:
                    logger.info('KeyboardInterrupt received.')
                    self._TeleBot__stop_polling.set()
                    break
                except Exception as e:
                    try:
                        if self.exception_handler is not None:
                            handled = self.exception_handler.handle(e)
                        else:
                            handled = False
                        if not handled:
                            raise e
                        else:
                            time.sleep(error_interval)
                    finally:
                        e = None
                        del e

        logger.info('Stopped polling.')

    def _exec_task(self, task, *args, **kwargs):
        if self.threaded:
            (self.worker_pool.put)(task, *args, **kwargs)
        else:
            task(*args, **kwargs)

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

    def send_message(self, chat_id, text, disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None, timeout=None):
        """
        Use this method to send text messages.

        Warning: Do not send more than about 4000 characters each message, otherwise you'll risk an HTTP 414 error.
        If you must send more than 4000 characters, use the split_string function in apihelper.py.

        :param chat_id:
        :param text:
        :param disable_web_page_preview:
        :param reply_to_message_id:
        :param reply_markup:
        :param parse_mode:
        :param disable_notification: Boolean, Optional. Sends the message silently.
        :param timeout:
        :return: API reply.
        """
        parse_mode = self.parse_mode if parse_mode is None else parse_mode
        return types.Message.de_json(apihelper.send_message(self.token, chat_id, text, disable_web_page_preview, reply_to_message_id, reply_markup, parse_mode, disable_notification, timeout))

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

    def copy_message(self, chat_id, from_chat_id, message_id, caption=None, parse_mode=None, caption_entities=None, disable_notification=None, reply_to_message_id=None, allow_sending_without_reply=None, reply_markup=None, timeout=None):
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

    def send_photo(self, chat_id, photo, caption=None, reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None, timeout=None):
        """
        Use this method to send photos.
        :param disable_notification:
        :param chat_id:
        :param photo:
        :param caption:
        :param parse_mode
        :param reply_to_message_id:
        :param reply_markup:
        :param timeout:
        :return: API reply.
        """
        parse_mode = self.parse_mode if parse_mode is None else parse_mode
        return types.Message.de_json(apihelper.send_photo(self.token, chat_id, photo, caption, reply_to_message_id, reply_markup, parse_mode, disable_notification, timeout))

    def send_audio(self, chat_id, audio, caption=None, duration=None, performer=None, title=None, reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None, timeout=None, thumb=None):
        """
        Use this method to send audio files, if you want Telegram clients to display them in the music player. Your audio must be in the .mp3 format.
        :param chat_id:Unique identifier for the message recipient
        :param audio:Audio file to send.
        :param caption:
        :param duration:Duration of the audio in seconds
        :param performer:Performer
        :param title:Track name
        :param reply_to_message_id:If the message is a reply, ID of the original message
        :param reply_markup:
        :param parse_mode
        :param disable_notification:
        :param timeout:
        :param thumb:
        :return: Message
        """
        parse_mode = self.parse_mode if parse_mode is None else parse_mode
        return types.Message.de_json(apihelper.send_audio(self.token, chat_id, audio, caption, duration, performer, title, reply_to_message_id, reply_markup, parse_mode, disable_notification, timeout, thumb))

    def send_voice(self, chat_id, voice, caption=None, duration=None, reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None, timeout=None):
        """
        Use this method to send audio files, if you want Telegram clients to display the file as a playable voice message.
        :param chat_id:Unique identifier for the message recipient.
        :param voice:
        :param caption:
        :param duration:Duration of sent audio in seconds
        :param reply_to_message_id:
        :param reply_markup:
        :param parse_mode
        :param disable_notification:
        :param timeout:
        :return: Message
        """
        parse_mode = self.parse_mode if parse_mode is None else parse_mode
        return types.Message.de_json(apihelper.send_voice(self.token, chat_id, voice, caption, duration, reply_to_message_id, reply_markup, parse_mode, disable_notification, timeout))

    def send_document(self, chat_id, data, reply_to_message_id=None, caption=None, reply_markup=None, parse_mode=None, disable_notification=None, timeout=None, thumb=None):
        """
        Use this method to send general files.
        :param chat_id:
        :param data:
        :param reply_to_message_id:
        :param caption:
        :param reply_markup:
        :param parse_mode:
        :param disable_notification:
        :param timeout:
        :param thumb: InputFile or String : Thumbnail of the file sent
        :return: API reply.
        """
        parse_mode = self.parse_mode if parse_mode is None else parse_mode
        return types.Message.de_json(apihelper.send_data(self.token, chat_id, data, 'document', reply_to_message_id, reply_markup, parse_mode, disable_notification, timeout, caption, thumb))

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

    def send_video(self, chat_id, data, duration=None, caption=None, reply_to_message_id=None, reply_markup=None, parse_mode=None, supports_streaming=None, disable_notification=None, timeout=None, thumb=None, width=None, height=None):
        """
        Use this method to send video files, Telegram clients support mp4 videos.
        :param chat_id: Integer : Unique identifier for the message recipient ??? User or GroupChat id
        :param data: InputFile or String : Video to send. You can either pass a file_id as String to resend a video that is already on the Telegram server
        :param duration: Integer : Duration of sent video in seconds
        :param caption: String : Video caption (may also be used when resending videos by file_id).
        :param parse_mode:
        :param supports_streaming:
        :param reply_to_message_id:
        :param reply_markup:
        :param disable_notification:
        :param timeout:
            :param thumb: InputFile or String : Thumbnail of the file sent
        :param width:
        :param height:
        :return:
        """
        parse_mode = self.parse_mode if parse_mode is None else parse_mode
        return types.Message.de_json(apihelper.send_video(self.token, chat_id, data, duration, caption, reply_to_message_id, reply_markup, parse_mode, supports_streaming, disable_notification, timeout, thumb, width, height))

    def send_animation(self, chat_id, animation, duration=None, caption=None, reply_to_message_id=None, reply_markup=None, parse_mode=None, disable_notification=None, timeout=None, thumb=None):
        """
        Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without sound).
        :param chat_id: Integer : Unique identifier for the message recipient ??? User or GroupChat id
        :param animation: InputFile or String : Animation to send. You can either pass a file_id as String to resend an animation that is already on the Telegram server
        :param duration: Integer : Duration of sent video in seconds
        :param caption: String : Animation caption (may also be used when resending animation by file_id).
        :param parse_mode:
        :param reply_to_message_id:
        :param reply_markup:
        :param disable_notification:
        :param timeout:
        :param thumb: InputFile or String : Thumbnail of the file sent
        :return:
        """
        parse_mode = self.parse_mode if parse_mode is None else parse_mode
        return types.Message.de_json(apihelper.send_animation(self.token, chat_id, animation, duration, caption, reply_to_message_id, reply_markup, parse_mode, disable_notification, timeout, thumb))

    def send_video_note(self, chat_id, data, duration=None, length=None, reply_to_message_id=None, reply_markup=None, disable_notification=None, timeout=None, thumb=None):
        """
        As of v.4.0, Telegram clients support rounded square mp4 videos of up to 1 minute long. Use this method to send video messages.
        :param chat_id: Integer : Unique identifier for the message recipient ??? User or GroupChat id
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
        return types.Message.de_json(apihelper.send_video_note(self.token, chat_id, data, duration, length, reply_to_message_id, reply_markup, disable_notification, timeout, thumb))

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
        return types.Message.de_json(apihelper.send_location(self.token, chat_id, latitude, longitude, live_period, reply_to_message_id, reply_markup, disable_notification, timeout))

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
        :param foursquare_type: Foursquare type of the venue, if known. (For example, ???arts_entertainment/default???, ???arts_entertainment/aquarium??? or ???food/icecream???.)
        :param disable_notification:
        :param reply_to_message_id:
        :param reply_markup:
        :param timeout:
        :return:
        """
        return types.Message.de_json(apihelper.send_venue(self.token, chat_id, latitude, longitude, title, address, foursquare_id, foursquare_type, disable_notification, reply_to_message_id, reply_markup, timeout))

    def send_contact(self, chat_id, phone_number, first_name, last_name=None, vcard=None, disable_notification=None, reply_to_message_id=None, reply_markup=None, timeout=None):
        return types.Message.de_json(apihelper.send_contact(self.token, chat_id, phone_number, first_name, last_name, vcard, disable_notification, reply_to_message_id, reply_markup, timeout))

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
        return apihelper.promote_chat_member(self.token, chat_id, user_id, can_change_info, can_post_messages, can_edit_messages, can_delete_messages, can_invite_users, can_restrict_members, can_pin_messages, can_promote_members)

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
        Note: In regular groups (non-supergroups), this method will only work if the ???All Members Are Admins???
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
        Note: In regular groups (non-supergroups), this method will only work if the ???All Members Are Admins???
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
        Note: In regular groups (non-supergroups), this method will only work if the ???All Members Are Admins???
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

    def edit_message_text(self, text, chat_id=None, message_id=None, inline_message_id=None, parse_mode=None, disable_web_page_preview=None, reply_markup=None):
        """
        Use this method to edit text and game messages.
        :param text:
        :param chat_id:
        :param message_id:
        :param inline_message_id:
        :param parse_mode:
        :param disable_web_page_preview:
        :param reply_markup:
        :return:
        """
        parse_mode = self.parse_mode if parse_mode is None else parse_mode
        result = apihelper.edit_message_text(self.token, text, chat_id, message_id, inline_message_id, parse_mode, disable_web_page_preview, reply_markup)
        if type(result) == bool:
            return result
        return types.Message.de_json(result)

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

    def edit_message_caption(self, caption, chat_id=None, message_id=None, inline_message_id=None, parse_mode=None, reply_markup=None):
        """
        Use this method to edit captions of messages
        :param caption:
        :param chat_id:
        :param message_id:
        :param inline_message_id:
        :param parse_mode:
        :param reply_markup:
        :return:
        """
        parse_mode = self.parse_mode if parse_mode is None else parse_mode
        result = apihelper.edit_message_caption(self.token, caption, chat_id, message_id, inline_message_id, parse_mode, reply_markup)
        if type(result) == bool:
            return result
        return types.Message.de_json(result)

    def reply_to(self, message, text, **kwargs):
        """
        Convenience function for `send_message(message.chat.id, text, reply_to_message_id=message.message_id, **kwargs)`
            :param message:
        :param text:
        :param kwargs:
        :return:
        """
        return (self.send_message)(message.chat.id, text, reply_to_message_id=message.message_id, **kwargs)

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

    def register_for_reply(self, message, callback, *args, **kwargs):
        """
        Registers a callback function to be notified when a reply to `message` arrives.

        Warning: In case `callback` as lambda function, saving reply handlers will not work.

        :param message:     The message for which we are awaiting a reply.
        :param callback:    The callback function to be called when a reply arrives. Must accept one `message`
                            parameter, which will contain the replied message.
        """
        message_id = message.message_id
        (self.register_for_reply_by_message_id)(message_id, callback, *args, **kwargs)

    def register_for_reply_by_message_id(self, message_id, callback, *args, **kwargs):
        """
        Registers a callback function to be notified when a reply to `message` arrives.

        Warning: In case `callback` as lambda function, saving reply handlers will not work.

        :param message_id:  The id of the message for which we are awaiting a reply.
        :param callback:    The callback function to be called when a reply arrives. Must accept one `message`
                            parameter, which will contain the replied message.
        """
        self.reply_backend.register_handler(message_id, Handler(callback, *args, **kwargs))

    def _notify_reply_handlers(self, new_messages):
        """
        Notify handlers of the answers
        :param new_messages:
        :return:
        """
        for message in new_messages:
            if hasattr(message, 'reply_to_message'):
                if message.reply_to_message is not None:
                    handlers = self.reply_backend.get_handlers(message.reply_to_message.message_id)
            if handlers:
                for handler in handlers:
                    (self._exec_task)(handler['callback'], message, *(handler['args']), **handler['kwargs'])

    def register_next_step_handler(self, message, callback, *args, **kwargs):
        """
        Registers a callback function to be notified when new message arrives after `message`.

        Warning: In case `callback` as lambda function, saving next step handlers will not work.

        :param message:     The message for which we want to handle new message in the same chat.
        :param callback:    The callback function which next new message arrives.
        :param args:        Args to pass in callback func
        :param kwargs:      Args to pass in callback func
        """
        chat_id = message.chat.id
        (self.register_next_step_handler_by_chat_id)(chat_id, callback, *args, **kwargs)

    def register_next_step_handler_by_chat_id(self, chat_id, callback, *args, **kwargs):
        """
        Registers a callback function to be notified when new message arrives after `message`.

        Warning: In case `callback` as lambda function, saving next step handlers will not work.

        :param chat_id:     The chat for which we want to handle new message.
        :param callback:    The callback function which next new message arrives.
        :param args:        Args to pass in callback func
        :param kwargs:      Args to pass in callback func
        """
        self.next_step_backend.register_handler(chat_id, Handler(callback, *args, **kwargs))

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

    def _notify_next_handlers(self, new_messages):
        """
        Description: TBD
        :param new_messages:
        :return:
        """
        for i, message in enumerate(new_messages):
            need_pop = False
            handlers = self.next_step_backend.get_handlers(message.chat.id)
            if handlers:
                for handler in handlers:
                    need_pop = True
                    (self._exec_task)(handler['callback'], message, *(handler['args']), **handler['kwargs'])
                else:
                    if need_pop:
                        new_messages.pop(i)

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

    def message_handler(self, commands=None, regexp=None, func=None, content_types=None, **kwargs):
        """
        Message handler decorator.
        This decorator can be used to decorate functions that must handle certain types of messages.
        All message handlers are tested in the order they were added.

        Example:

        bot = TeleBot('TOKEN')

        # Handles all messages which text matches regexp.
        @bot.message_handler(regexp='someregexp')
        def command_help(message):
            bot.send_message(message.chat.id, 'Did someone call for help?')

        # Handle all sent documents of type 'text/plain'.
        @bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
        def command_handle_document(message):
            bot.send_message(message.chat.id, 'Document received, sir!')

        # Handle all other messages.
        @bot.message_handler(func=lambda message: True, content_types=['audio', 'photo', 'voice', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
        def default_command(message):
            bot.send_message(message.chat.id, "This is the default command handler.")

        :param commands: Optional list of strings (commands to handle).
        :param regexp: Optional regular expression.
        :param func: Optional lambda function. The lambda receives the message to test as the first parameter. It must return True if the command should handle the message.
        :param content_types: Supported message content types. Must be a list. Defaults to ['text'].
        """
        if content_types is None:
            content_types = [
             'text']

        def decorator(handler):
            handler_dict = (self._build_handler_dict)(handler, content_types=content_types, 
             commands=commands, 
             regexp=regexp, 
             func=func, **kwargs)
            self.add_message_handler(handler_dict)
            return handler

        return decorator

    def add_message_handler(self, handler_dict):
        """
        Adds a message handler
        :param handler_dict:
        :return:
        """
        self.message_handlers.append(handler_dict)

    def edited_message_handler(self, commands=None, regexp=None, func=None, content_types=None, **kwargs):
        """
        Edit message handler decorator
        :param commands:
        :param regexp:
        :param func:
        :param content_types:
        :param kwargs:
        :return:
        """
        if content_types is None:
            content_types = [
             'text']

        def decorator(handler):
            handler_dict = (self._build_handler_dict)(handler, commands=commands, 
             regexp=regexp, 
             func=func, 
             content_types=content_types, **kwargs)
            self.add_edited_message_handler(handler_dict)
            return handler

        return decorator

    def add_edited_message_handler(self, handler_dict):
        """
        Adds the edit message handler
        :param handler_dict:
        :return:
        """
        self.edited_message_handlers.append(handler_dict)

    def channel_post_handler(self, commands=None, regexp=None, func=None, content_types=None, **kwargs):
        """
        Channel post handler decorator
        :param commands:
        :param regexp:
        :param func:
        :param content_types:
        :param kwargs:
        :return:
        """
        if content_types is None:
            content_types = [
             'text']

        def decorator(handler):
            handler_dict = (self._build_handler_dict)(handler, commands=commands, 
             regexp=regexp, 
             func=func, 
             content_types=content_types, **kwargs)
            self.add_channel_post_handler(handler_dict)
            return handler

        return decorator

    def add_channel_post_handler(self, handler_dict):
        """
        Adds channel post handler
        :param handler_dict:
        :return:
        """
        self.channel_post_handlers.append(handler_dict)

    def edited_channel_post_handler(self, commands=None, regexp=None, func=None, content_types=None, **kwargs):
        """
        Edit channel post handler decorator
        :param commands:
        :param regexp:
        :param func:
        :param content_types:
        :param kwargs:
        :return:
        """
        if content_types is None:
            content_types = [
             'text']

        def decorator(handler):
            handler_dict = (self._build_handler_dict)(handler, commands=commands, 
             regexp=regexp, 
             func=func, 
             content_types=content_types, **kwargs)
            self.add_edited_channel_post_handler(handler_dict)
            return handler

        return decorator

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

        def decorator(handler):
            handler_dict = (self._build_handler_dict)(handler, func=func, **kwargs)
            self.add_inline_handler(handler_dict)
            return handler

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

        def decorator(handler):
            handler_dict = (self._build_handler_dict)(handler, func=func, **kwargs)
            self.add_chosen_inline_handler(handler_dict)
            return handler

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

        def decorator(handler):
            handler_dict = (self._build_handler_dict)(handler, func=func, **kwargs)
            self.add_callback_query_handler(handler_dict)
            return handler

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

        def decorator(handler):
            handler_dict = (self._build_handler_dict)(handler, func=func, **kwargs)
            self.add_shipping_query_handler(handler_dict)
            return handler

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

        def decorator(handler):
            handler_dict = (self._build_handler_dict)(handler, func=func, **kwargs)
            self.add_pre_checkout_query_handler(handler_dict)
            return handler

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

        def decorator(handler):
            handler_dict = (self._build_handler_dict)(handler, func=func, **kwargs)
            self.add_poll_handler(handler_dict)
            return handler

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

        def decorator(handler):
            handler_dict = (self._build_handler_dict)(handler, func=func, **kwargs)
            self.add_poll_answer_handler(handler_dict)
            return handler

        return decorator

    def add_poll_answer_handler(self, handler_dict):
        """
        Adds a poll_answer request handler
        :param handler_dict:
        :return:
        """
        self.poll_answer_handlers.append(handler_dict)

    def _test_message_handler(self, message_handler, message):
        """
        Test message handler
        :param message_handler:
        :param message:
        :return:
        """
        for message_filter, filter_value in message_handler['filters'].items():
            if filter_value is None:
                pass
            else:
                if not self._test_filter(message_filter, filter_value, message):
                    return False
        else:
            return True

    @staticmethod
    def _test_filter(message_filter, filter_value, message):
        """
        Test filters
        :param message_filter:
        :param filter_value:
        :param message:
        :return:
        """
        test_cases = {'content_types':lambda msg: msg.content_type in filter_value, 
         'regexp':lambda msg: msg.content_type == 'text' and re.search(filter_value, msg.text, re.IGNORECASE), 
         'commands':lambda msg: msg.content_type == 'text' and util.extract_command(msg.text) in filter_value, 
         'func':lambda msg: filter_value(msg)}
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

    def __init__(self, *args, **kwargs):
        (TeleBot.__init__)(self, *args, **kwargs)

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
    def get_file(self, *args):
        return (TeleBot.get_file)(self, *args)

    @util.async_dec()
    def download_file(self, *args):
        return (TeleBot.download_file)(self, *args)

    @util.async_dec()
    def get_user_profile_photos(self, *args, **kwargs):
        return (TeleBot.get_user_profile_photos)(self, *args, **kwargs)

    @util.async_dec()
    def get_chat(self, *args):
        return (TeleBot.get_chat)(self, *args)

    @util.async_dec()
    def leave_chat(self, *args):
        return (TeleBot.leave_chat)(self, *args)

    @util.async_dec()
    def get_chat_administrators(self, *args):
        return (TeleBot.get_chat_administrators)(self, *args)

    @util.async_dec()
    def get_chat_members_count(self, *args):
        return (TeleBot.get_chat_members_count)(self, *args)

    @util.async_dec()
    def set_chat_sticker_set(self, *args):
        return (TeleBot.set_chat_sticker_set)(self, *args)

    @util.async_dec()
    def delete_chat_sticker_set(self, *args):
        return (TeleBot.delete_chat_sticker_set)(self, *args)

    @util.async_dec()
    def get_chat_member(self, *args):
        return (TeleBot.get_chat_member)(self, *args)

    @util.async_dec()
    def send_message(self, *args, **kwargs):
        return (TeleBot.send_message)(self, *args, **kwargs)

    @util.async_dec()
    def send_dice(self, *args, **kwargs):
        return (TeleBot.send_dice)(self, *args, **kwargs)

    @util.async_dec()
    def forward_message(self, *args, **kwargs):
        return (TeleBot.forward_message)(self, *args, **kwargs)

    @util.async_dec()
    def copy_message(self, *args, **kwargs):
        return (TeleBot.copy_message)(self, *args, **kwargs)

    @util.async_dec()
    def delete_message(self, *args):
        return (TeleBot.delete_message)(self, *args)

    @util.async_dec()
    def send_photo(self, *args, **kwargs):
        return (TeleBot.send_photo)(self, *args, **kwargs)

    @util.async_dec()
    def send_audio(self, *args, **kwargs):
        return (TeleBot.send_audio)(self, *args, **kwargs)

    @util.async_dec()
    def send_voice(self, *args, **kwargs):
        return (TeleBot.send_voice)(self, *args, **kwargs)

    @util.async_dec()
    def send_document(self, *args, **kwargs):
        return (TeleBot.send_document)(self, *args, **kwargs)

    @util.async_dec()
    def send_sticker(self, *args, **kwargs):
        return (TeleBot.send_sticker)(self, *args, **kwargs)

    @util.async_dec()
    def send_video(self, *args, **kwargs):
        return (TeleBot.send_video)(self, *args, **kwargs)

    @util.async_dec()
    def send_video_note(self, *args, **kwargs):
        return (TeleBot.send_video_note)(self, *args, **kwargs)

    @util.async_dec()
    def send_media_group(self, *args, **kwargs):
        return (TeleBot.send_media_group)(self, *args, **kwargs)

    @util.async_dec()
    def send_location(self, *args, **kwargs):
        return (TeleBot.send_location)(self, *args, **kwargs)

    @util.async_dec()
    def edit_message_live_location(self, *args, **kwargs):
        return (TeleBot.edit_message_live_location)(self, *args, **kwargs)

    @util.async_dec()
    def stop_message_live_location(self, *args, **kwargs):
        return (TeleBot.stop_message_live_location)(self, *args, **kwargs)

    @util.async_dec()
    def send_venue(self, *args, **kwargs):
        return (TeleBot.send_venue)(self, *args, **kwargs)

    @util.async_dec()
    def send_contact(self, *args, **kwargs):
        return (TeleBot.send_contact)(self, *args, **kwargs)

    @util.async_dec()
    def send_chat_action(self, *args, **kwargs):
        return (TeleBot.send_chat_action)(self, *args, **kwargs)

    @util.async_dec()
    def kick_chat_member(self, *args, **kwargs):
        return (TeleBot.kick_chat_member)(self, *args, **kwargs)

    @util.async_dec()
    def unban_chat_member(self, *args, **kwargs):
        return (TeleBot.unban_chat_member)(self, *args, **kwargs)

    @util.async_dec()
    def restrict_chat_member(self, *args, **kwargs):
        return (TeleBot.restrict_chat_member)(self, *args, **kwargs)

    @util.async_dec()
    def promote_chat_member(self, *args, **kwargs):
        return (TeleBot.promote_chat_member)(self, *args, **kwargs)

    @util.async_dec()
    def export_chat_invite_link(self, *args):
        return (TeleBot.export_chat_invite_link)(self, *args)

    @util.async_dec()
    def set_chat_photo(self, *args):
        return (TeleBot.set_chat_photo)(self, *args)

    @util.async_dec()
    def delete_chat_photo(self, *args):
        return (TeleBot.delete_chat_photo)(self, *args)

    @util.async_dec()
    def set_chat_title(self, *args):
        return (TeleBot.set_chat_title)(self, *args)

    @util.async_dec()
    def set_chat_description(self, *args):
        return (TeleBot.set_chat_description)(self, *args)

    @util.async_dec()
    def pin_chat_message(self, *args, **kwargs):
        return (TeleBot.pin_chat_message)(self, *args, **kwargs)

    @util.async_dec()
    def unpin_chat_message(self, *args):
        return (TeleBot.unpin_chat_message)(self, *args)

    @util.async_dec()
    def unpin_all_chat_messages(self, *args):
        return (TeleBot.unpin_all_chat_messages)(self, *args)

    @util.async_dec()
    def edit_message_text(self, *args, **kwargs):
        return (TeleBot.edit_message_text)(self, *args, **kwargs)

    @util.async_dec()
    def edit_message_media(self, *args, **kwargs):
        return (TeleBot.edit_message_media)(self, *args, **kwargs)

    @util.async_dec()
    def edit_message_reply_markup(self, *args, **kwargs):
        return (TeleBot.edit_message_reply_markup)(self, *args, **kwargs)

    @util.async_dec()
    def send_game(self, *args, **kwargs):
        return (TeleBot.send_game)(self, *args, **kwargs)

    @util.async_dec()
    def set_game_score(self, *args, **kwargs):
        return (TeleBot.set_game_score)(self, *args, **kwargs)

    @util.async_dec()
    def get_game_high_scores(self, *args, **kwargs):
        return (TeleBot.get_game_high_scores)(self, *args, **kwargs)

    @util.async_dec()
    def send_invoice(self, *args, **kwargs):
        return (TeleBot.send_invoice)(self, *args, **kwargs)

    @util.async_dec()
    def answer_shipping_query(self, *args, **kwargs):
        return (TeleBot.answer_shipping_query)(self, *args, **kwargs)

    @util.async_dec()
    def answer_pre_checkout_query(self, *args, **kwargs):
        return (TeleBot.answer_pre_checkout_query)(self, *args, **kwargs)

    @util.async_dec()
    def edit_message_caption(self, *args, **kwargs):
        return (TeleBot.edit_message_caption)(self, *args, **kwargs)

    @util.async_dec()
    def answer_inline_query(self, *args, **kwargs):
        return (TeleBot.answer_inline_query)(self, *args, **kwargs)

    @util.async_dec()
    def answer_callback_query(self, *args, **kwargs):
        return (TeleBot.answer_callback_query)(self, *args, **kwargs)

    @util.async_dec()
    def get_sticker_set(self, *args, **kwargs):
        return (TeleBot.get_sticker_set)(self, *args, **kwargs)

    @util.async_dec()
    def upload_sticker_file(self, *args, **kwargs):
        return (TeleBot.upload_sticker_file)(self, *args, **kwargs)

    @util.async_dec()
    def create_new_sticker_set(self, *args, **kwargs):
        return (TeleBot.create_new_sticker_set)(self, *args, **kwargs)

    @util.async_dec()
    def add_sticker_to_set(self, *args, **kwargs):
        return (TeleBot.add_sticker_to_set)(self, *args, **kwargs)

    @util.async_dec()
    def set_sticker_position_in_set(self, *args, **kwargs):
        return (TeleBot.set_sticker_position_in_set)(self, *args, **kwargs)

    @util.async_dec()
    def delete_sticker_from_set(self, *args, **kwargs):
        return (TeleBot.delete_sticker_from_set)(self, *args, **kwargs)

    @util.async_dec()
    def send_poll(self, *args, **kwargs):
        return (TeleBot.send_poll)(self, *args, **kwargs)

    @util.async_dec()
    def stop_poll(self, *args, **kwargs):
        return (TeleBot.stop_poll)(self, *args, **kwargs)