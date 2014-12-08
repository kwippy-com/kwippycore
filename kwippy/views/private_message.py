from django.conf import settings
from django.contrib.auth.models import User
from kwippy.models.account import Account
from kwippy.views.mykwips import isfollowing
from kwippy.views.comm_queue import send_mail,send_im
from kwippy.models.private_message import Private_Message
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.simple import redirect_to
from kwippyproject.kwippy.models.list_filter import List_Filter
from kwippyproject.kwippy.models.spam_filter import Spam_Filter
from kwippyproject.kwippy.models.sent_filter import Sent_Filter
from kwippyproject.kwippy.views.mykwips import details_for_kwips_page, isfollowing
from kwippy.views.main import comment_count, kwip_count, is_in_group
from django.contrib.auth.decorators import login_required
from django import template, http
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect

@login_required
def pvt_message(request, receiver):
    """This function will store pvt msgs in db
        and send a notification mail to receiver"""    
    if request.method == "POST":
        referer = request.META.get('HTTP_REFERER', '')
        sender = request.user
        receiver_username =  request.POST.get('receiver_username', False) 
        receiver = get_object_or_404(User, username=receiver_username)
        msg = request.POST.get('pvt_msg', False) 
        account = get_object_or_404(Account, user=sender, provider=0)
        if isfollowing(receiver, sender) or is_in_group(sender,'team'):
            if sender.is_active == 4:
                request.session['flash'] = "You are temporarily not allowed to message someone. Please contact support@kwippy.com"
                return redirect_to(request, referer)
            message = Private_Message(sender=sender, receiver=receiver,
                                  message=msg, account=account)
            message.save()
            list_filter = List_Filter(receiver_user = receiver, pm = message,status=0)
            list_filter.save()
            sent_filter = Sent_Filter(sender_user = sender, pm = message)
            sent_filter.save()
            request.session['flash'] = "Your private message was sent"
            params_for_mail = {'#_1':receiver.username,'#_2':sender.username, '#_3':msg, '#_4':str(message.id)}
            send_mail(str(receiver.email), 'kwippy <support@kwippy.com>', 'private_message', params_for_mail)
            send_im(receiver,'private_message', params_for_mail)
            return redirect_to(request, referer)
        else:
            request.session['flash'] = "You cannot send this message"
            return redirect_to(request, referer)

@login_required
def reply_pvt_msg(request):
    """This function will store pvt msgs in db
        and send a notification mail to receiver"""
    sender = request.user
    receiver = get_object_or_404(User, username=str(request.GET['receiver']))
    msg = str(request.GET['pvt_msg'])
    account = get_object_or_404(Account, user=sender, provider=0)
    if isfollowing(receiver, sender) or is_in_group(receiver,'team'):
        if sender.is_active == 4:
            json = simplejson.dumps(['not allowed'])
            return HttpResponse(json,mimetype='application/json')
        message = Private_Message(sender=sender, receiver=receiver,
                                  message=msg, account=account)
        message.save()
        list_filter = List_Filter(receiver_user = receiver, pm = message,status=0)
        list_filter.save()
        sent_filter = Sent_Filter(sender_user = sender, pm = message)
        sent_filter.save()        
        params_for_mail = {'#_1':receiver.username,'#_2':sender.username, '#_3':msg, '#_4':str(message.id)}
        send_mail(str(receiver.email), 'kwippy <support@kwippy.com>', 'private_message', params_for_mail)
        send_im(receiver,'private_message', params_for_mail)
	json = simplejson.dumps(['sent'])
	return HttpResponse(json,mimetype='application/json')

def view(request, msg_id):
    #dict = details_for_kwips_page(request,request.user.username)    
    message = get_object_or_404(List_Filter, pm=int(msg_id))
    sender_is_team = is_in_group(message.pm.sender,'team')
    if request.user == message.receiver_user:
        message.status=1
        message.save()
        unread_incoming_msgs = List_Filter.objects.filter(receiver_user=int(request.user.id), status=0).count()
        is_following = isfollowing(message.pm.sender,request.user)
        return render_to_response('messages/view.html', {'login': request.user.username,'message': message,
                              'unread_incoming_msgs':unread_incoming_msgs,'is_following':is_following,'sender_is_team':sender_is_team,
                              'revision_number': settings.REVISION_NUMBER,}, context_instance=template.RequestContext(request))
    else:
        referer = '/' + str(request.user.username) + '/messages/inbox/'
        return HttpResponseRedirect(referer)
    
@login_required
def view_outbox(request, msg_id):
    message = get_object_or_404(Sent_Filter, pm=int(msg_id))
    if request.user == message.sender_user:
        unread_incoming_msgs = List_Filter.objects.filter(receiver_user=int(request.user.id), status=0).count()
        return render_to_response('messages/view_outbox.html', {'login': request.user.username,'message': message,
                             'unread_incoming_msgs':unread_incoming_msgs,
                              'revision_number': settings.REVISION_NUMBER,}, context_instance=template.RequestContext(request))
    else:
        referer = '/' + str(request.user.username) + '/messages/outbox/'
        return HttpResponseRedirect(referer)
        

@login_required
def delete_from_inbox(request, msg_id):
    message = get_object_or_404(List_Filter, pm=int(msg_id))
    message.delete()  
    request.session['flash'] = "Your private message was deleted"
    referer = '/'+request.user.username+'/messages/inbox'
    return HttpResponseRedirect(referer)

@login_required
def delete_from_outbox(request, msg_id):
    message = get_object_or_404(Sent_Filter, pm=int(msg_id))
    message.delete()  
    request.session['flash'] = "Your private message was deleted"
    referer = '/'+request.user.username+'/messages/outbox'
    return HttpResponseRedirect(referer)


@login_required
def read(request, receiver,msg):
    # Fill code to mark it as read
    referer = request.META.get('HTTP_REFERER', '')
    request.session['flash'] = "Your private message was marked as read"
    return redirect_to(request, referer)

@login_required
def unread(request, receiver,msg):
    # Fill code to mark it as unread
    referer = request.META.get('HTTP_REFERER', '')
    request.session['flash'] = "Your private message was marked as unread"
    return redirect_to(request, referer)
