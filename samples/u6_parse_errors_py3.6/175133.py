# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: electrum\gui\qt\update_checker.py
import asyncio, base64
from distutils.version import StrictVersion
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar, QHBoxLayout, QPushButton
from electrum import version
from electrum import constants
from electrum import ecc
from electrum.i18n import _
from electrum.util import PrintError, make_aiohttp_session

class UpdateCheck(QWidget, PrintError):
    url = 'https://electrum.org/version'
    download_url = 'https://electrum.org/#download'
    VERSION_ANNOUNCEMENT_SIGNING_KEYS = ('13xjmVAB1EATPP8RshTE8S8sNwwSUM9p1P', )

    def __init__(self, main_window, latest_version=None):
        self.main_window = main_window
        QWidget.__init__(self)
        self.setWindowTitle('Electrum - ' + _('Update Check'))
        self.content = QVBoxLayout()
        (self.content.setContentsMargins)(*[10] * 4)
        self.heading_label = QLabel()
        self.content.addWidget(self.heading_label)
        self.detail_label = QLabel()
        self.detail_label.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.detail_label.setOpenExternalLinks(True)
        self.content.addWidget(self.detail_label)
        self.pb = QProgressBar()
        self.pb.setMaximum(0)
        self.pb.setMinimum(0)
        self.content.addWidget(self.pb)
        versions = QHBoxLayout()
        versions.addWidget(QLabel(_('Current version: {}'.format(version.ELECTRUM_VERSION))))
        self.latest_version_label = QLabel(_('Latest version: {}'.format(' ')))
        versions.addWidget(self.latest_version_label)
        self.content.addLayout(versions)
        self.update_view(latest_version)
        self.update_check_thread = UpdateCheckThread(self.main_window)
        self.update_check_thread.checked.connect(self.on_version_retrieved)
        self.update_check_thread.failed.connect(self.on_retrieval_failed)
        self.update_check_thread.start()
        close_button = QPushButton(_('Close'))
        close_button.clicked.connect(self.close)
        self.content.addWidget(close_button)
        self.setLayout(self.content)

    def on_version_retrieved(self, version):
        self.update_view(version)

    def on_retrieval_failed(self):
        self.heading_label.setText('<h2>' + _('Update check failed') + '</h2>')
        self.detail_label.setText(_('Sorry, but we were unable to check for updates. Please try again later.'))
        self.pb.hide()

    @staticmethod
    def is_newer(latest_version):
        return latest_version > StrictVersion(version.ELECTRUM_VERSION)

    def update_view(self, latest_version=None):
        if latest_version:
            self.pb.hide()
            self.latest_version_label.setText(_('Latest version: {}'.format(latest_version)))
            if self.is_newer(latest_version):
                self.heading_label.setText('<h2>' + _('There is a new update available') + '</h2>')
                url = "<a href='{u}'>{u}</a>".format(u=(UpdateCheck.download_url))
                self.detail_label.setText(_('You can download the new version from {}.').format(url))
            else:
                self.heading_label.setText('<h2>' + _('Already up to date') + '</h2>')
                self.detail_label.setText(_('You are already on the latest version of Electrum.'))
        else:
            self.heading_label.setText('<h2>' + _('Checking for updates...') + '</h2>')
            self.detail_label.setText(_('Please wait while Electrum checks for available updates.'))


class UpdateCheckThread(QThread, PrintError):
    checked = pyqtSignal(object)
    failed = pyqtSignal()

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    async def get_update_info--- This code section failed: ---

 L. 104         0  LOAD_GLOBAL              make_aiohttp_session
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                main_window
                6  LOAD_ATTR                network
                8  LOAD_ATTR                proxy
               10  LOAD_CONST               ('proxy',)
               12  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               14  BEFORE_ASYNC_WITH
               16  GET_AWAITABLE    
               18  LOAD_CONST               None
               20  YIELD_FROM       
               22  SETUP_ASYNC_WITH    218  'to 218'
               24  STORE_FAST               'session'

 L. 105        26  LOAD_FAST                'session'
               28  LOAD_ATTR                get
               30  LOAD_GLOBAL              UpdateCheck
               32  LOAD_ATTR                url
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  BEFORE_ASYNC_WITH
               38  GET_AWAITABLE    
               40  LOAD_CONST               None
               42  YIELD_FROM       
               44  SETUP_ASYNC_WITH    202  'to 202'
               46  STORE_FAST               'result'

 L. 106        48  LOAD_FAST                'result'
               50  LOAD_ATTR                json
               52  LOAD_CONST               None
               54  LOAD_CONST               ('content_type',)
               56  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               58  GET_AWAITABLE    
               60  LOAD_CONST               None
               62  YIELD_FROM       
               64  STORE_FAST               'signed_version_dict'

 L. 114        66  LOAD_FAST                'signed_version_dict'
               68  LOAD_STR                 'version'
               70  BINARY_SUBSCR    
               72  STORE_FAST               'version_num'

 L. 115        74  LOAD_FAST                'signed_version_dict'
               76  LOAD_STR                 'signatures'
               78  BINARY_SUBSCR    
               80  STORE_FAST               'sigs'

 L. 116        82  SETUP_LOOP          190  'to 190'
               84  LOAD_FAST                'sigs'
               86  LOAD_ATTR                items
               88  CALL_FUNCTION_0       0  '0 positional arguments'
               90  GET_ITER         
               92  FOR_ITER            180  'to 180'
               94  UNPACK_SEQUENCE_2     2 
               96  STORE_FAST               'address'
               98  STORE_FAST               'sig'

 L. 117       100  LOAD_FAST                'address'
              102  LOAD_GLOBAL              UpdateCheck
              104  LOAD_ATTR                VERSION_ANNOUNCEMENT_SIGNING_KEYS
              106  COMPARE_OP               not-in
              108  POP_JUMP_IF_FALSE   112  'to 112'

 L. 118       110  CONTINUE             92  'to 92'
              112  ELSE                     '178'

 L. 119       112  LOAD_GLOBAL              base64
              114  LOAD_ATTR                b64decode
              116  LOAD_FAST                'sig'
              118  CALL_FUNCTION_1       1  '1 positional argument'
              120  STORE_FAST               'sig'

 L. 120       122  LOAD_FAST                'version_num'
              124  LOAD_ATTR                encode
              126  LOAD_STR                 'utf-8'
              128  CALL_FUNCTION_1       1  '1 positional argument'
              130  STORE_FAST               'msg'

 L. 121       132  LOAD_GLOBAL              ecc
              134  LOAD_ATTR                verify_message_with_address
              136  LOAD_FAST                'address'
              138  LOAD_FAST                'sig'
              140  LOAD_FAST                'msg'

 L. 122       142  LOAD_GLOBAL              constants
              144  LOAD_ATTR                BitcoinMainnet
              146  LOAD_CONST               ('address', 'sig65', 'message', 'net')
              148  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              150  POP_JUMP_IF_FALSE    92  'to 92'

 L. 123       152  LOAD_FAST                'self'
              154  LOAD_ATTR                print_error
              156  LOAD_STR                 "valid sig for version announcement '"
              158  LOAD_FAST                'version_num'
              160  FORMAT_VALUE          0  ''
              162  LOAD_STR                 "' from address '"
              164  LOAD_FAST                'address'
              166  FORMAT_VALUE          0  ''
              168  LOAD_STR                 "'"
              170  BUILD_STRING_5        5 
              172  CALL_FUNCTION_1       1  '1 positional argument'
              174  POP_TOP          

 L. 124       176  BREAK_LOOP       
            178_0  COME_FROM           150  '150'
              178  JUMP_BACK            92  'to 92'
              180  POP_BLOCK        

 L. 126       182  LOAD_GLOBAL              Exception
              184  LOAD_STR                 'no valid signature for version announcement'
              186  CALL_FUNCTION_1       1  '1 positional argument'
              188  RAISE_VARARGS_1       1  'exception'
            190_0  COME_FROM_LOOP       82  '82'

 L. 127       190  LOAD_GLOBAL              StrictVersion
              192  LOAD_FAST                'version_num'
              194  LOAD_ATTR                strip
              196  CALL_FUNCTION_0       0  '0 positional arguments'
              198  CALL_FUNCTION_1       1  '1 positional argument'
              200  RETURN_VALUE     
            202_0  COME_FROM_ASYNC_WITH    44  '44'
              202  WITH_CLEANUP_START
              204  GET_AWAITABLE    
              206  LOAD_CONST               None
              208  YIELD_FROM       
              210  WITH_CLEANUP_FINISH
              212  END_FINALLY      
              214  POP_BLOCK        
              216  LOAD_CONST               None
            218_0  COME_FROM_ASYNC_WITH    22  '22'
              218  WITH_CLEANUP_START
              220  GET_AWAITABLE    
              222  LOAD_CONST               None
              224  YIELD_FROM       
              226  WITH_CLEANUP_FINISH
              228  END_FINALLY      

Parse error at or near `COME_FROM_ASYNC_WITH' instruction at offset 202_0

    def run(self):
        network = self.main_window.network
        if not network:
            self.failed.emit()
            return
        try:
            update_info = asyncio.run_coroutine_threadsafe(self.get_update_info(), network.asyncio_loop).result()
        except Exception as e:
            self.print_error(f"got exception: '{repr(e)}'")
            self.failed.emit()
        else:
            self.checked.emit(update_info)