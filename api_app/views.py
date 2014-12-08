from kwippy.models.quip import Quip
from kwippy.models.account import Account
from kwippy.models.user_profile import User_Profile
from kwippy.models.notification_setting import NotificationSetting
from kwippy.models.page_setting import PageSetting
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import *
from httpauth import *
from xmlgen import *
import simplejson
import sha
import random
import re

def return_error(request,text,type):
    if type=="xml":
        r = xml.ret(xml.user(request.user.username),xml.error(text))
        res = HttpResponseBadRequest(makeXml(r),mimetype='text/xml; charset=utf-8')
    elif type=="json":
        r = simplejson.dumps([{'user':request.user.username},{'error':text}])
        res = HttpResponseBadRequest(r,mimetype='application/json')
    return res

def return_success(request,text,type):
    if type=="xml":
        r = xml.ret(xml.user(request.user.username),xml.success(text))
        res = HttpResponse(makeXml(r),mimetype='text/xml; charset=utf-8')
    elif type=="json":
        r = simplejson.dumps([{'user':request.user.username},{'success':text}])
        res = HttpResponse(r,mimetype='application/json')
    return res

@logged_in_or_basicauth()
def post_kwip(request,type):
    if request.method == 'POST':
        vendor = 10 # Default vendor is API
        if request.POST.has_key('validate'):
            if request.POST['validate']=='1':
                return return_success(request,"The user has been validated.",type)
        if not request.POST.has_key('kwip'):
            return return_error(request,"Bad Request: you have not sent a kwip",type)
        if request.POST.has_key('vendor'):
            try:
                vendor = int(request.POST['vendor'])
            except ValueError:
                return return_error(request,"Bad Request: you have not sent a illegal vendor ID",type)
        if vendor<=11:
            return return_error(request,"Bad Request: you have not sent a illegal vendor ID",type)
            
        # Sent vendor ID create a new account for it
        acc = Account.objects.filter(user=request.user,provider=vendor)
        if not acc:
            acc = [Account(provider_login=request.user.username,provider=vendor,user=request.user,registration_type=2,status=1)]
            acc[0].save()
        quip = Quip(original=request.POST['kwip'].replace("\\",""),formated=request.POST['kwip'].replace("\\",""),account=acc[0],user=request.user,is_filtered=1)
        quip.save()
        user_pro = User_Profile.objects.filter(user=request.user)
        user_pro = user_pro[0]
        user_pro.quip_total = user_pro.quip_total + 1
        user_pro.save()
        return return_success(request,"The kwip has been successfully posted.",type)
    return return_error(request,"Bad Request: This call only supports a POST request.",type)

# posting an SMS
def post_sms(request,country_name):
    if request.method=="GET":
        # country specific code
        if country_name=="venezuela":
            shortcode = request.GET.get("shortcode","0") 
            command = request.GET.get("command","0")
            message = request.GET.get("message","0")
            caller = request.GET.get("caller","0")
            telco = request.GET.get("telco","0")
            other_param = "58 | " + shortcode + " | " + command + " | " + telco
            # Check if this caller is registered
            if not (caller.startswith("058") and caller.startswith("58")):
                caller = "58" + caller
            acc = Account.objects.filter(provider_login=caller,provider=11)
            if not acc:
            # if not , register him using his number
                cuser = User(username=caller,email=caller+"@kwippy.com")
                cuser.set_password(caller+telco)
                cuser.save()
                cpagesetting = PageSetting(user=cuser,show_repeat=True)
                cpagesetting.save()
                not_setting = NotificationSetting(user=cuser)
                not_setting.save()
                random_hash = sha.new(str(cuser.email)+str(random.random())).hexdigest()[:10]
                cprofile = User_Profile(user=cuser,display_name=caller,hash=random_hash)
                cprofile.save()
                acc = [Account(user=cuser,provider_login=caller,provider=11,status=1,other_param=other_param)]
                acc[0].save()            
                acc1 = Account(user=cuser,provider_login=caller,provider=0,status=1)
                acc1.save()
            # if registered post his message on his user
            quip = Quip(original=message.replace("\\",""),formated=message.replace("\\",""),account=acc[0],user=acc[0].user,is_filtered=1)
            quip.save()
            user_pro = User_Profile.objects.filter(user=acc[0].user)
            user_pro = user_pro[0]
            user_pro.quip_total = user_pro.quip_total + 1
            user_pro.save()
        return HttpResponse("")
    return HttpResponse("")

