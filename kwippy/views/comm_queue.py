#This function should be called to make inserts into the command queue table
import pdb
from django.contrib.auth.models import User
from kwippy.models.account import Account
from kwippyproject.comm_queue_app.models import *
from kwippyproject.kwippy.models.email import Email
from kwippyproject.kwippy.models.im import IM
from django.shortcuts import get_object_or_404,get_list_or_404
from django.conf import settings

def comm_queue(type,obj_type,params):
    comm_queue = Commd(type=type,status=0,params=params,obj_type=obj_type)
    comm_queue.save()
            
def send_mail_old(receipient, sender, subject, text, html):    
    params = receipient + '||'    
    params = params + sender + '||'
    params = params + subject + '||'
    params = params + text + '||'
    params = params + html + '||'
    params = params + '0'
    comm_queue(0,0,params)     

def send_im(receipient_user, type, params):
    accounts = Account.objects.filter(user=receipient_user,provider=2)
    parameters = ''
    if accounts:
        account=accounts[0]
        im = get_object_or_404(IM, type=type)
        body_text = im.body
        parameters = account.provider_login + '||'
        if len(body_text):
            for i in range(1,len(params)+1):
                i = '#_' + str(i)
                body_text = body_text.replace(i,params[i])
        body_text = body_text.replace('ssiittee',settings.SITE)
        parameters = parameters + body_text + '||'
        parameters = parameters + str(receipient_user.id)
        # add some code to handle the case when either text or html is ''
        # replacing #'s with respective dynamic parameters
        if type == 'comment':
            im_type = 1
        elif type == 'follower':
            im_type = 2
        elif type == 'private_message':
            im_type = 3
        elif type == 'buzz':
            im_type = 4
        elif type == 'comment_follower':
            im_type = 1
        elif type == 'kwip':
            im_type = 5
        elif type == 'favorite_kwip':
            im_type = 6
        elif type == 'friend_request':
            im_type = 7
        elif type == 'invite_to_talk':
            im_type = 8
        else:
            im_type = 0
        comm_queue(4,im_type,parameters)
    
def send_mail(receipient, sender, type, params):
    if type not in ('friend_invite','beta_invite','contactus','invite_to_talk_anon','comment_follower_anon','email_activation'):
        receipient_user = get_object_or_404(User, email=receipient)
        receipient_user_id = receipient_user.id
    else:
        receipient_user_id = 0
    email = get_object_or_404(Email, type=type)            
    if valid_params(email.body_html,params):
        parameters = receipient + '||'    
        parameters = parameters + sender + '||'    
        subject = email.subject
        body_text = email.body_text
        body_html = email.body_html
        if len(subject):            
            for i in range(1,len(params)+1):
                i = '#_' + str(i)                
                subject = subject.replace(i,params[i])        
        parameters = parameters + subject + '||'        
        if len(body_text):
            for i in range(1,len(params)+1):
                i = '#_' + str(i)
                body_text = body_text.replace(i,params[i])
        body_text = body_text.replace('ssiittee',settings.SITE)
        body_text = body_text + get_object_or_404(Email, type='footer').body_text            
        parameters = parameters + body_text + '||'
        if len(body_html):            
            for i in range(1,len(params)+1):
                i = '#_' + str(i)
                body_html = body_html.replace(i,params[i])
        body_html = body_html.replace('ssiittee',settings.SITE)
        body_html = body_html + get_object_or_404(Email, type='footer').body_html            
        parameters = parameters + body_html + '||'
        parameters = parameters + str(receipient_user_id)
    # add some code to handle the case when either text or html is ''
    # replacing #'s with respective dynamic parameters    
    if type == 'comment':
        mail_type = 1
    elif type == 'follower':
        mail_type = 2
    elif type == 'private_message':
        mail_type = 3
    elif type == 'buzz':
        mail_type = 4
    elif type == 'favorite_kwip':
        mail_type = 6        
    elif type == 'friend_request':
        mail_type = 7
    elif type == 'invite_to_talk':
        mail_type = 8
    #elif type == 'invite_to_talk_anon':
    #    mail_type = 9
    #elif type == 'comment_follower_anon':
    #    mail_type = 10            
    elif type == 'birthday':
        mail_type = 0
    elif type == 'comment_follower':
        mail_type = 1
    else:
        mail_type = 0
    comm_queue(0,mail_type,parameters) 

def valid_params(string,data_dict):
    no_err = 1
    for i in range(1,len(data_dict)+1):
        i = '#_' + str(i)
        if not string.count(i):
            no_err=0    
    return no_err

       
