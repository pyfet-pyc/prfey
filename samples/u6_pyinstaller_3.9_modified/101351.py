# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Jun 29 2021, 19:54:56) 
# [GCC 8.3.0]
# Embedded file name: unittest\_log.py
import logging, collections
from .case import _BaseTestCaseContext
_LoggingWatcher = collections.namedtuple('_LoggingWatcher', [
 'records', 'output'])

class _CapturingHandler(logging.Handler):
    __doc__ = '\n    A logging handler capturing all (raw and formatted) logging output.\n    '

    def __init__(self):
        logging.Handler.__init__(self)
        self.watcher = _LoggingWatcher([], [])

    def flush(self):
        pass

    def emit(self, record):
        self.watcher.records.append(record)
        msg = self.format(record)
        self.watcher.output.append(msg)


class _AssertLogsContext(_BaseTestCaseContext):
    __doc__ = 'A context manager used to implement TestCase.assertLogs().'
    LOGGING_FORMAT = '%(levelname)s:%(name)s:%(message)s'

    def __init__(self, test_case, logger_name, level):
        _BaseTestCaseContext.__init__(self, test_case)
        self.logger_name = logger_name
        if level:
            self.level = logging._nameToLevel.get(level, level)
        else:
            self.level = logging.INFO
        self.msg = None

    def __enter__(self):
        if isinstance(self.logger_name, logging.Logger):
            logger = self.logger = self.logger_name
        else:
            logger = self.logger = logging.getLogger(self.logger_name)
        formatter = logging.Formatter(self.LOGGING_FORMAT)
        handler = _CapturingHandler()
        handler.setFormatter(formatter)
        self.watcher = handler.watcher
        self.old_handlers = logger.handlers[:]
        self.old_level = logger.level
        self.old_propagate = logger.propagate
        logger.handlers = [handler]
        logger.setLevel(self.level)
        logger.propagate = False
        return handler.watcher

    def __exit__--- This code section failed: ---

 L.  60         0  LOAD_FAST                'self'
                2  LOAD_ATTR                old_handlers
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                logger
                8  STORE_ATTR               handlers

 L.  61        10  LOAD_FAST                'self'
               12  LOAD_ATTR                old_propagate
               14  LOAD_FAST                'self'
               16  LOAD_ATTR                logger
               18  STORE_ATTR               propagate

 L.  62        20  LOAD_FAST                'self'
               22  LOAD_ATTR                logger
               24  LOAD_METHOD              setLevel
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                old_level
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          

 L.  63        34  LOAD_FAST                'exc_type'
               36  LOAD_CONST               None
               38  <117>                 1  ''
               40  POP_JUMP_IF_FALSE    46  'to 46'

 L.  65        42  LOAD_CONST               False
               44  RETURN_VALUE     
             46_0  COME_FROM            40  '40'

 L.  66        46  LOAD_GLOBAL              len
               48  LOAD_FAST                'self'
               50  LOAD_ATTR                watcher
               52  LOAD_ATTR                records
               54  CALL_FUNCTION_1       1  ''
               56  LOAD_CONST               0
               58  COMPARE_OP               ==
               60  POP_JUMP_IF_FALSE    92  'to 92'

 L.  67        62  LOAD_FAST                'self'
               64  LOAD_METHOD              _raiseFailure

 L.  68        66  LOAD_STR                 'no logs of level {} or higher triggered on {}'
               68  LOAD_METHOD              format

 L.  69        70  LOAD_GLOBAL              logging
               72  LOAD_METHOD              getLevelName
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                level
               78  CALL_METHOD_1         1  ''
               80  LOAD_FAST                'self'
               82  LOAD_ATTR                logger
               84  LOAD_ATTR                name

 L.  68        86  CALL_METHOD_2         2  ''

 L.  67        88  CALL_METHOD_1         1  ''
               90  POP_TOP          
             92_0  COME_FROM            60  '60'

Parse error at or near `<117>' instruction at offset 38