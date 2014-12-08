from django.shortcuts import render_to_response
from django.template import RequestContext
from django import template
from django.http import HttpResponseRedirect
from kwippyproject.kwippy.models.contact_us import ContactUs
from kwippyproject.comm_queue_app.models import *
from kwippy.views.comm_queue import send_mail

def contactus(request):
    if request.method == "POST":
        if request.user.is_authenticated():
            message=request.POST['msg']
            contact = ContactUs(senders_email=str(request.user.email), message=message, senders_user_id=int(request.user.id))
            contact.save()
            params_for_mail = {'#_1':request.user.username,'#_2':request.user.email, '#_3':message, '#_4':request.user.username}
            send_mail('feedback@kwippy.com','kwippy <support@kwippy.com>','contactus',params_for_mail)            
       	    request.session['flash'] = 'Thanks for contacting us.'
	    return HttpResponseRedirect('/home/contactus/')	
	else:
            senders_email=str(request.POST['email']).strip()
            message=request.POST['msg'].strip()
            contact = ContactUs(senders_email=senders_email, message=message)
            contact.save()
            params_for_mail = {'#_1':'non registered user','#_2':senders_email, '#_3':message, '#_4':'non registered user'}
            send_mail('feedback@kwippy.com','kwippy <support@kwippy.com>','contactus',params_for_mail)                        
            request.session['flash'] = 'Thanks for contacting us'
            return HttpResponseRedirect('/home/contactus/')
    return render_to_response('contactus.html', context_instance=template.RequestContext(request))
