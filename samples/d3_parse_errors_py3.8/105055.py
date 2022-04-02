# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: site-packages\win32\lib\win32evtlogutil.py
"""Event Log Utilities - helper for win32evtlog.pyd
"""
import win32api, win32con, winerror, win32evtlog
error = win32api.error
langid = win32api.MAKELANGID(win32con.LANG_NEUTRAL, win32con.SUBLANG_NEUTRAL)

def AddSourceToRegistry(appName, msgDLL=None, eventLogType='Application', eventLogFlags=None):
    """Add a source of messages to the event log.

    Allows Python program to register a custom source of messages in the
    registry.  You must also provide the DLL name that has the message table, so the
    full message text appears in the event log.

    Note that the win32evtlog.pyd file has a number of string entries with just "%1"
    built in, so many Python programs can simply use this DLL.  Disadvantages are that
    you do not get language translation, and the full text is stored in the event log,
    blowing the size of the log up.
    """
    if msgDLL is None:
        msgDLL = win32evtlog.__file__
    hkey = win32api.RegCreateKey(win32con.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Services\\EventLog\\%s\\%s' % (eventLogType, appName))
    win32api.RegSetValueEx(hkey, 'EventMessageFile', 0, win32con.REG_EXPAND_SZ, msgDLL)
    if eventLogFlags is None:
        eventLogFlags = win32evtlog.EVENTLOG_ERROR_TYPE | win32evtlog.EVENTLOG_WARNING_TYPE | win32evtlog.EVENTLOG_INFORMATION_TYPE
    win32api.RegSetValueEx(hkey, 'TypesSupported', 0, win32con.REG_DWORD, eventLogFlags)
    win32api.RegCloseKey(hkey)


def RemoveSourceFromRegistry(appName, eventLogType='Application'):
    """Removes a source of messages from the event log.
    """
    try:
        win32api.RegDeleteKey(win32con.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Services\\EventLog\\%s\\%s' % (eventLogType, appName))
    except win32api.error as exc:
        try:
            if exc.winerror != winerror.ERROR_FILE_NOT_FOUND:
                raise
        finally:
            exc = None
            del exc


def ReportEvent(appName, eventID, eventCategory=0, eventType=win32evtlog.EVENTLOG_ERROR_TYPE, strings=None, data=None, sid=None):
    """Report an event for a previously added event source.
    """
    hAppLog = win32evtlog.RegisterEventSource(None, appName)
    win32evtlog.ReportEvent(hAppLog, eventType, eventCategory, eventID, sid, strings, data)
    win32evtlog.DeregisterEventSource(hAppLog)


def FormatMessage--- This code section failed: ---

 L.  97         0  LOAD_STR                 'SYSTEM\\CurrentControlSet\\Services\\EventLog\\%s\\%s'
                2  LOAD_FAST                'logType'
                4  LOAD_FAST                'eventLogRecord'
                6  LOAD_ATTR                SourceName
                8  BUILD_TUPLE_2         2 
               10  BINARY_MODULO    
               12  STORE_FAST               'keyName'

 L. 101        14  LOAD_GLOBAL              win32api
               16  LOAD_METHOD              RegOpenKey
               18  LOAD_GLOBAL              win32con
               20  LOAD_ATTR                HKEY_LOCAL_MACHINE
               22  LOAD_FAST                'keyName'
               24  CALL_METHOD_2         2  ''
               26  STORE_FAST               'handle'

 L. 102        28  SETUP_FINALLY       178  'to 178'

 L. 103        30  LOAD_GLOBAL              win32api
               32  LOAD_METHOD              RegQueryValueEx
               34  LOAD_FAST                'handle'
               36  LOAD_STR                 'EventMessageFile'
               38  CALL_METHOD_2         2  ''
               40  LOAD_CONST               0
               42  BINARY_SUBSCR    
               44  LOAD_METHOD              split
               46  LOAD_STR                 ';'
               48  CALL_METHOD_1         1  ''
               50  STORE_FAST               'dllNames'

 L. 105        52  LOAD_CONST               None
               54  STORE_FAST               'data'

 L. 106        56  LOAD_FAST                'dllNames'
               58  GET_ITER         
             60_0  COME_FROM           172  '172'
             60_1  COME_FROM           166  '166'
               60  FOR_ITER            174  'to 174'
               62  STORE_FAST               'dllName'

 L. 107        64  SETUP_FINALLY       138  'to 138'

 L. 110        66  LOAD_GLOBAL              win32api
               68  LOAD_METHOD              ExpandEnvironmentStrings
               70  LOAD_FAST                'dllName'
               72  CALL_METHOD_1         1  ''
               74  STORE_FAST               'dllName'

 L. 112        76  LOAD_GLOBAL              win32api
               78  LOAD_METHOD              LoadLibraryEx
               80  LOAD_FAST                'dllName'
               82  LOAD_CONST               0
               84  LOAD_GLOBAL              win32con
               86  LOAD_ATTR                LOAD_LIBRARY_AS_DATAFILE
               88  CALL_METHOD_3         3  ''
               90  STORE_FAST               'dllHandle'

 L. 113        92  SETUP_FINALLY       122  'to 122'

 L. 114        94  LOAD_GLOBAL              win32api
               96  LOAD_METHOD              FormatMessageW
               98  LOAD_GLOBAL              win32con
              100  LOAD_ATTR                FORMAT_MESSAGE_FROM_HMODULE

 L. 115       102  LOAD_FAST                'dllHandle'

 L. 115       104  LOAD_FAST                'eventLogRecord'
              106  LOAD_ATTR                EventID

 L. 115       108  LOAD_GLOBAL              langid

 L. 115       110  LOAD_FAST                'eventLogRecord'
              112  LOAD_ATTR                StringInserts

 L. 114       114  CALL_METHOD_5         5  ''
              116  STORE_FAST               'data'
              118  POP_BLOCK        
              120  BEGIN_FINALLY    
            122_0  COME_FROM_FINALLY    92  '92'

 L. 117       122  LOAD_GLOBAL              win32api
              124  LOAD_METHOD              FreeLibrary
              126  LOAD_FAST                'dllHandle'
              128  CALL_METHOD_1         1  ''
              130  POP_TOP          
              132  END_FINALLY      
              134  POP_BLOCK        
              136  JUMP_FORWARD        160  'to 160'
            138_0  COME_FROM_FINALLY    64  '64'

 L. 118       138  DUP_TOP          
              140  LOAD_GLOBAL              win32api
              142  LOAD_ATTR                error
              144  COMPARE_OP               exception-match
              146  POP_JUMP_IF_FALSE   158  'to 158'
              148  POP_TOP          
              150  POP_TOP          
              152  POP_TOP          

 L. 119       154  POP_EXCEPT       
              156  BREAK_LOOP          160  'to 160'
            158_0  COME_FROM           146  '146'
              158  END_FINALLY      
            160_0  COME_FROM           156  '156'
            160_1  COME_FROM           136  '136'

 L. 120       160  LOAD_FAST                'data'
              162  LOAD_CONST               None
              164  COMPARE_OP               is-not
              166  POP_JUMP_IF_FALSE_BACK    60  'to 60'

 L. 121       168  POP_TOP          
              170  BREAK_LOOP          174  'to 174'
              172  JUMP_BACK            60  'to 60'
            174_0  COME_FROM           170  '170'
            174_1  COME_FROM            60  '60'
              174  POP_BLOCK        
              176  BEGIN_FINALLY    
            178_0  COME_FROM_FINALLY    28  '28'

 L. 123       178  LOAD_GLOBAL              win32api
              180  LOAD_METHOD              RegCloseKey
              182  LOAD_FAST                'handle'
              184  CALL_METHOD_1         1  ''
              186  POP_TOP          
              188  END_FINALLY      

 L. 124       190  LOAD_FAST                'data'
              192  JUMP_IF_TRUE_OR_POP   196  'to 196'
              194  LOAD_STR                 ''
            196_0  COME_FROM           192  '192'
              196  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `END_FINALLY' instruction at offset 158


def SafeFormatMessage(eventLogRecord, logType=None):
    """As for FormatMessage, except returns an error message if
    the message can not be processed.
    """
    if logType is None:
        logType = 'Application'
    try:
        return FormatMessage(eventLogRecord, logType)
    except win32api.error:
        if eventLogRecord.StringInserts is None:
            desc = ''
        else:
            desc = ', '.join(eventLogRecord.StringInserts)
        return '<The description for Event ID ( %d ) in Source ( %r ) could not be found. It contains the following insertion string(s):%r.>' % (winerror.HRESULT_CODE(eventLogRecord.EventID), eventLogRecord.SourceName, desc)


def FeedEventLogRecords(feeder, machineName=None, logName='Application', readFlags=None):
    if readFlags is None:
        readFlags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    h = win32evtlog.OpenEventLog(machineName, logName)
    try:
        while True:
            objects = win32evtlog.ReadEventLoghreadFlags0
            if not objects:
                pass
            else:
                map(lambda item, feeder=feeder: feeder(item*()), objects)

    finally:
        win32evtlog.CloseEventLog(h)