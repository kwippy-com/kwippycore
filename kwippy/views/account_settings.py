import os,pdb, random, sha
from django import forms, template, http
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import  HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from kwippy.views.main import get_display_name
from kwippyproject.kwippy.models.user_profile import User_Profile
from kwippyproject.kwippy.models.email_account import Email_Account
from kwippyproject.kwippy.models.notification_setting import NotificationSetting
from kwippyproject.kwippy.forms.auth_forms import  PasswordChangeForm
from kwippy.views.comm_queue import send_mail

def check_key(request, key):
    if request.POST.has_key(key):
        result = str(1)
    else:
        result = str(0)
    return result


@login_required
def account(request, template_name = "dashboard/dashboard_account.html"):    
    referer = request.META['PATH_INFO']
    if str(referer.split('/')[1])!=str(request.user.username):
        return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/')
    new_data, errors = {}, {}
    displayname = get_display_name(request.user)
    user = request.user
    not_settings = get_object_or_404(NotificationSetting, user=int(request.user.id))
    if request.method == "POST":
        # save notification settings
        form = PasswordChangeForm()
        form.set_user(request.user)
        secondary_email = ''
        csv = ''
        csv = csv + check_key(request, 'comment_mail') + ','+ check_key(request, 'follower_mail') + ','
        csv = csv + check_key(request, 'pm_mail') + ','+ check_key(request, 'buzz_mail')  + ',' + '0' + ',' + check_key(request, 'fav_mail') + ',' + check_key(request, 'fr_req_mail') + ',' + check_key(request, 'conv_inv_mail')
        not_settings.email = csv
        not_settings.save()
        csv = not_settings.email.split(',')
        comment_mail = int(csv[0])
        follower_mail = int(csv[1])
        pm_mail   = int(csv[2])
        buzz_mail = int(csv[3])
	fav_mail = int(csv[5])
        fr_req_mail = int(csv[6])
        conv_inv_mail = int(csv[7])
        csv = ''
        csv = csv + check_key(request, 'comment_im') + ','+ check_key(request, 'follower_im') + ','
        csv = csv + check_key(request, 'pm_im') + ','+ check_key(request, 'buzz_im') + ',' + check_key(request, 'kwips_im') + ',' + check_key(request, 'fav_im') + ',' + check_key(request, 'fr_req_im') + ',' + check_key(request, 'conv_inv_im')
        not_settings.im = csv
        not_settings.save()
        csv = not_settings.im.split(',')
        comment_im = int(csv[0])
        follower_im = int(csv[1])
        pm_im   = int(csv[2])
        buzz_im = int(csv[3])
        kwips_im = int(csv[4])
	fav_im = int(csv[5])
        fr_req_im = int(csv[6])
        conv_inv_im = int(csv[7])
        user_profile = get_object_or_404(User_Profile, user=user)
        user_profile.default_notification_on = int(request.POST['def_im_notification'])
        user_profile.save()
        default_notification_on = user_profile.default_notification_on
        if request.POST.has_key('secondary_mail') and request.POST['secondary_mail'] != 'enter email id':
            secondary_email = str(request.POST['secondary_mail'])
            if secondary_email != user.email:
                code = sha.new(secondary_email+str(random.random())).hexdigest()[:10]
                email_acc = Email_Account(email=secondary_email,user=user,status=0,code=code)
                email_acc.save()                                      
                send_mail(secondary_email,'support@kwippy.com','email_activation',{'#_1':user.username,'#_2':code})
                secondary_email = get_object_or_404(Email_Account,user=user)
            else:
                secondary_email = ''
        elif request.POST.has_key('commn_email'):
            email_acc = get_object_or_404(Email_Account,user=user)
            if str(request.POST['commn_email']) != user.email and email_acc.status == 1:
                temp_email = user.email
                user.email = str(request.POST['commn_email'])
                user.save()
                email_acc.email = temp_email
                email_acc.save()
                secondary_email = email_acc
            else:
                secondary_email = get_object_or_404(Email_Account,user=user)
        if request.POST['old_password']!='' or request.POST['new_password1']!='' or request.POST['new_password2']!='':
            form = PasswordChangeForm(request.POST)
            form.set_user(request.user)
            new_data = request.POST.copy()
            if not form.errors:
                form.save(new_data)
                request.session['flash'] = "Changes saved"
                return render_to_response('dashboard/dashboard_account.html', { 'form': form ,'displayname':displayname,'comment_mail': comment_mail,'secondary_email':secondary_email,
                                  'follower_mail': follower_mail,'pm_mail':pm_mail, 'buzz_mail':buzz_mail, 'fav_mail': fav_mail, 'fr_req_mail': fr_req_mail, 'comment_im': comment_im,
                                  'follower_im': follower_im,'default_notification_on':default_notification_on, 'pm_im':pm_im,'buzz_im':buzz_im,'kwips_im':kwips_im,'fav_im': fav_im, 'fr_req_im': fr_req_im, 'conv_inv_im': conv_inv_im},context_instance=template.RequestContext(request))
            return render_to_response('dashboard/dashboard_account.html', {'form': form,'displayname':displayname,
                        'comment_mail': comment_mail, 'follower_mail': follower_mail,'pm_mail':pm_mail,'buzz_mail':buzz_mail,'fav_mail':fav_mail,'fr_req_mail':fr_req_mail,'default_notification_on':default_notification_on,
		        'comment_im': comment_im,'follower_im': follower_im, 'pm_im':pm_im,'buzz_im':buzz_im,'kwips_im':kwips_im,'fav_im':fav_im,'fr_req_im':fr_req_im,'conv_inv_im':conv_inv_im}, context_instance=template.RequestContext(request))
        else:
            request.session['flash'] = "Changes saved" 
        return render_to_response('dashboard/dashboard_account.html', { 'form': form ,'displayname':displayname,'comment_mail': comment_mail,'secondary_email':secondary_email,
                                  'follower_mail': follower_mail,'pm_mail':pm_mail, 'buzz_mail':buzz_mail,'fav_mail':fav_mail,'fr_req_mail':fr_req_mail,'conv_inv_mail':conv_inv_mail,'comment_im': comment_im,
                                   'follower_im': follower_im, 'pm_im':pm_im,'buzz_im':buzz_im,'kwips_im':kwips_im, 'fav_im':fav_im,'fr_req_im': fr_req_im,'default_notification_on':default_notification_on, 'conv_inv_im':conv_inv_im},context_instance=template.RequestContext(request))     

    else:
        csv = not_settings.email.split(',')
        comment_mail = int(csv[0])
        follower_mail = int(csv[1])
        pm_mail   = int(csv[2])
        buzz_mail = int(csv[3])
	fav_mail = int(csv[5])
        fr_req_mail = int(csv[6])
        conv_inv_mail = int(csv[7])
        csv_im = not_settings.im.split(',')
        comment_im = int(csv_im[0])
        follower_im = int(csv_im[1])
        pm_im   = int(csv_im[2])
        buzz_im = int(csv_im[3])
        kwips_im = int(csv_im[4])        
	fav_im = int(csv_im[5])
        fr_req_im = int(csv_im[6])
        conv_inv_im = int(csv_im[7])
        default_notification_on = get_object_or_404(User_Profile, user=user).default_notification_on
        secondary_email = Email_Account.objects.filter(user=user)
        form = PasswordChangeForm()
        form.set_user(request.user)
        if secondary_email:
            secondary_email = secondary_email[0]
        return render_to_response('dashboard/dashboard_account.html', { 'form': form ,'displayname': displayname, 'comment_mail': comment_mail,'secondary_email':secondary_email,
                                  'follower_mail': follower_mail,'pm_mail':pm_mail, 'buzz_mail':buzz_mail, 'fav_mail': fav_mail,'fr_req_mail':fr_req_mail,'conv_inv_mail': conv_inv_mail,
                                  'comment_im': comment_im, 'follower_im': follower_im, 'pm_im':pm_im,'buzz_im':buzz_im,'kwips_im':kwips_im,'default_notification_on':default_notification_on,'fav_im': fav_im,'fr_req_im':fr_req_im,'conv_inv_im':conv_inv_im, },context_instance=template.RequestContext(request))     
  

  
