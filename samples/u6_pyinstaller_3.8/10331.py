# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: win32evtlogutil.py
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


def FormatMessage(eventLogRecord, logType='Application'):
    """Given a tuple from ReadEventLog, and optionally where the event
    record came from, load the message, and process message inserts.

    Note that this function may raise win32api.error.  See also the
    function SafeFormatMessage which will return None if the message can
    not be processed.
    """
    keyName = 'SYSTEM\\CurrentControlSet\\Services\\EventLog\\%s\\%s' % (logType, eventLogRecord.SourceName)
    handle = win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE, keyName)
    try:
        dllNames = win32api.RegQueryValueEx(handle, 'EventMessageFile')[0].split(';')
        data = None
        for dllName in dllNames:
            try:
                dllName = win32api.ExpandEnvironmentStrings(dllName)
                dllHandle = win32api.LoadLibraryEx(dllName, 0, win32con.LOAD_LIBRARY_AS_DATAFILE)
                try:
                    data = win32api.FormatMessageW(win32con.FORMAT_MESSAGE_FROM_HMODULE, dllHandle, eventLogRecord.EventID, langid, eventLogRecord.StringInserts)
                finally:
                    win32api.FreeLibrary(dllHandle)

            except win32api.error:
                pass
            else:
                if data is not None:
                    break

    finally:
        win32api.RegCloseKey(handle)

    return data or ''


def SafeFormatMessage--- This code section failed: ---

 L. 130         0  LOAD_FAST                'logType'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 130         8  LOAD_STR                 'Application'
               10  STORE_FAST               'logType'
             12_0  COME_FROM             6  '6'

 L. 131        12  SETUP_FINALLY        26  'to 26'

 L. 132        14  LOAD_GLOBAL              FormatMessage
               16  LOAD_FAST                'eventLogRecord'
               18  LOAD_FAST                'logType'
               20  CALL_FUNCTION_2       2  ''
               22  POP_BLOCK        
               24  RETURN_VALUE     
             26_0  COME_FROM_FINALLY    12  '12'

 L. 133        26  DUP_TOP          
               28  LOAD_GLOBAL              win32api
               30  LOAD_ATTR                error
               32  COMPARE_OP               exception-match
               34  POP_JUMP_IF_FALSE    98  'to 98'
               36  POP_TOP          
               38  POP_TOP          
               40  POP_TOP          

 L. 134        42  LOAD_FAST                'eventLogRecord'
               44  LOAD_ATTR                StringInserts
               46  LOAD_CONST               None
               48  COMPARE_OP               is
               50  POP_JUMP_IF_FALSE    58  'to 58'

 L. 135        52  LOAD_STR                 ''
               54  STORE_FAST               'desc'
               56  JUMP_FORWARD         70  'to 70'
             58_0  COME_FROM            50  '50'

 L. 137        58  LOAD_STR                 ', '
               60  LOAD_METHOD              join
               62  LOAD_FAST                'eventLogRecord'
               64  LOAD_ATTR                StringInserts
               66  CALL_METHOD_1         1  ''
               68  STORE_FAST               'desc'
             70_0  COME_FROM            56  '56'

 L. 138        70  LOAD_STR                 '<The description for Event ID ( %d ) in Source ( %r ) could not be found. It contains the following insertion string(s):%r.>'
               72  LOAD_GLOBAL              winerror
               74  LOAD_METHOD              HRESULT_CODE
               76  LOAD_FAST                'eventLogRecord'
               78  LOAD_ATTR                EventID
               80  CALL_METHOD_1         1  ''
               82  LOAD_FAST                'eventLogRecord'
               84  LOAD_ATTR                SourceName
               86  LOAD_FAST                'desc'
               88  BUILD_TUPLE_3         3 
               90  BINARY_MODULO    
               92  ROT_FOUR         
               94  POP_EXCEPT       
               96  RETURN_VALUE     
             98_0  COME_FROM            34  '34'
               98  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 38


def FeedEventLogRecords(feeder, machineName=None, logName='Application', readFlags=None):
    if readFlags is None:
        readFlags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    h = win32evtlog.OpenEventLog(machineName, logName)
    try:
        while True:
            objects = win32evtlog.ReadEventLog(h, readFlags, 0)
            if not objects:
                break
            map(lambda item, feeder=feeder: feeder(item*()))objects

    finally:
        win32evtlog.CloseEventLog(h)