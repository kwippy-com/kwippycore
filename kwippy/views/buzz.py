"""This views will have functions
    for Buzz Messages"""
from django.contrib.auth.models import User
from kwippy.models.account import Account
from kwippy.views.mykwips import isfollowing
from kwippy.views.comm_queue import send_mail,send_im
from kwippy.views.main import get_display_name
from kwippy.models.buzz import Buzz
from django.shortcuts import get_object_or_404
from django.views.generic.simple import redirect_to


def buzz(request, receiver):
    """This function will store buzz msgs in db
        and send a notification mail to receiver"""    
    if request.method == "POST":
        referer = request.META.get('HTTP_REFERER', '')
        sender = request.user
        receiver_username =  request.POST.get('buzz_receiver', False) 
        receiver = get_object_or_404(User, username=receiver_username)
        buzz_msg = request.POST.get('buzz', False) 
        account = get_object_or_404(Account, user=sender, provider=0)
	buzz_type = int(request.POST.get('buzz_type', False))
        if isfollowing(receiver, sender):            
            buzz = Buzz(sender=sender, receiver=receiver,
                                  message=buzz_msg, buzz_type=buzz_type, account=account)
            buzz.save()
            request.session['flash'] = "Your buzz was sent !!"
            params_for_mail = {'#_1':get_display_name(receiver),'#_2':get_display_name(sender), '#_3':buzz_msg, '#_4':sender.username}
	    if buzz_type ==1:
		    send_mail(str(receiver.email), str(get_display_name(sender))+' <support@kwippy.com>', 'buzz', params_for_mail)
            	    send_im(receiver,'buzz', params_for_mail)
	    elif buzz_type ==2:
		    send_mail(str(receiver.email), str(get_display_name(sender))+' <support@kwippy.com>', 'photo_buzz', params_for_mail)
            	    send_im(receiver,'photo_buzz', params_for_mail)
            return redirect_to(request, referer)
        
        
    
	
