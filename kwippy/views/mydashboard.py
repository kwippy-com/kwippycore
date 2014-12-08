import os,pdb
from django import template, http
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from kwippy.views.main import get_display_name
from kwippyproject.kwippy.models.user_profile import User_Profile
from kwippyproject.kwippy.models.theme import Theme
from kwippyproject.kwippy.models.fireeagle import Fireeagle
from kwippyproject.kwippy.models.page_setting import PageSetting
from kwippyproject.kwippy.models.invite import Invite
#from kwippyproject.kwippy.models.email_notification_setting import Email_Notification_Setting
from kwippyproject.kwippy.forms.page_setting_form import Page_SettingForm
from kwippyproject.kwippy.forms.user_profile_form import *
from kwippyproject.kwippy.forms.auth_forms import  PasswordChangeForm
from kwippyproject.otherService.twitterService import getFollowers,sendDM
from console_app.views import generate_otherservice_invites,store_twitter_invite_in_db
from django.core.cache import cache
from django.contrib.auth.models import User
from kwippyproject.oi.inviter import *
from kwippyproject.console_app.views import *

@login_required
def import_ims(request, template_name = "dashboard/dashboard_import.html"):    
    referer = request.META['PATH_INFO']
    if str(referer.split('/')[1])!=str(request.user.username):
        return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/')
    new_data, errors = {}, {}
    user_profile = get_object_or_404(User_Profile, user=int(request.user.id))
    displayname = get_display_name(request.user)
    return render_to_response('dashboard/dashboard_import.html', { 'displayname':displayname,'user_profile': user_profile,},context_instance=template.RequestContext(request))     

@login_required
def invite_friends(request, template_name = "dashboard/invite_credentials.html"):    
    referer = request.META['PATH_INFO']
    if str(referer.split('/')[1])!=str(request.user.username):
        return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/invite')
    user_profile = get_object_or_404(User_Profile, user=int(request.user.id))
    displayname = get_display_name(request.user)
    if request.method == "POST":
        sample_data = getcontacts(request.POST['provider'],request.POST['twitter_username'],request.POST['twitter_password'])
        data = sample_data['contacts']
        registered_list = [] 
        if len(data)==0:
            request.session['flash'] = "Wrong username or password"
            return render_to_response('dashboard/invite_credentials.html', {'displayname':request.user, 'user_profile': user_profile,'login':request.user}, context_instance=template.RequestContext(request))                
        else:
            characters_allowed = 52 - len(request.user.username)
            characters_left = characters_allowed - 30
            return render_to_response('dashboard/invite_details.html', {'displayname':request.user, 'user_profile': user_profile,'data':data,'characters_left':characters_left, 'login':request.user,'characters_allowed':characters_allowed,'registered_list':registered_list,'username':request.POST['twitter_username'],'service':request.POST['provider'],'sessionid':sample_data['sessionid']},context_instance=template.RequestContext(request))                                           
    return render_to_response('dashboard/invite_credentials.html', 
    {'displayname':request.user, 'user_profile': user_profile,                                                          'login':request.user}, context_instance=template.RequestContext(request))     
        
@login_required
def send_invites(request, template_name = "dashboard/invite_credentials.html"):    
    referer = request.META['PATH_INFO']
    if str(referer.split('/')[1])!=str(request.user.username):
        return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/invite/')
    user_profile = get_object_or_404(User_Profile, user=int(request.user.id))
    displayname = get_display_name(request.user)
    if request.method == "POST":
        people = {}
        for item in request.POST:
            if item[:6]=='invite':
                people[item[7:]]=item[7:]
        sendmessage(request,request.POST["service"],request.POST["sessionid"],people)
        if not request.session['first_login'] == True:
            request.session['flash'] = "Invites have been added to the queue and will be sent shortly"
            return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/invite/')
            #return render_to_response('dashboard/invite_credentials.html', {'displayname':request.user, 'user_profile': user_profile,'login':request.user,}, context_instance=template.RequestContext(request))
        else:
            return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/profile/')  
    return render_to_response('dashboard/invite_credentials.html', {'displayname':request.user, 'user_profile': user_profile,
                                                           'login':request.user,},
                              context_instance=template.RequestContext(request))     


@login_required
def account(request, template_name = "dashboard/dashboard_account.html"):    
    referer = request.META['PATH_INFO']
    if str(referer.split('/')[1])!=str(request.user.username):
        return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/account/')
    new_data, errors = {}, {}
    displayname = get_display_name(request.user)
    form = PasswordChangeForm(request.user)
    if request.method == "POST":
            new_data = request.POST.copy()
            errors = form.get_validation_errors(new_data)
            if not errors:
                form.save(new_data)        
                request.session['flash'] = "Changes saved" 
                return render_to_response('dashboard/dashboard_account.html', { 'form': form ,'displayname':displayname,},context_instance=template.RequestContext(request))     
            return render_to_response('dashboard/dashboard_account.html', {'form': oldforms.FormWrapper(form, new_data, errors),'displayname':displayname,}, context_instance=template.RequestContext(request))
    else:
        return render_to_response('dashboard/dashboard_account.html', { 'form': form ,'displayname':displayname,},context_instance=template.RequestContext(request))	
  
@login_required
def kwips_page_settings(request, template_name = "dashboard/kwips_page.html"):    
    referer = request.META['PATH_INFO']
    if str(referer.split('/')[1])!=str(request.user.username):
        return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/kwips_page/')
    new_data, errors = {}, {}
    displayname = get_display_name(request.user)
    page_setting = get_object_or_404(PageSetting, user=int(request.user.id))
    user_profile = get_object_or_404(User_Profile, user=int(request.user.id))
    theme_list = Theme.objects.filter(id__in=range(1,10)).order_by('id')
    if not user_profile.theme_id:
        user_profile.theme_id=0
        user_profile.save()
    if request.method == "POST":
        page_setting.show_repeat=int(request.POST['hide_repeat'])
        page_setting.save()
        user_profile.theme_id=int(request.POST['theme_type'])
        user_profile.save()
        request.session['flash'] = "Changes saved"
        cache_key = '%s_profilequery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,request.user.id,)
        cache.delete(cache_key)
        cache_key = '%s_profilequeryname%s' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,request.user.username,)
        cache.delete(cache_key)
        form = Page_SettingForm(instance=page_setting)
        return render_to_response('dashboard/kwips_page.html', { 'form': form ,'displayname':displayname, 'show_repeats': page_setting.show_repeat, 'theme_list':theme_list, 'selected_theme':user_profile.theme_id},context_instance=template.RequestContext(request))             
    else:
        form = Page_SettingForm(instance=page_setting)
        return render_to_response('dashboard/kwips_page.html', { 'form': form ,'displayname':displayname, 'show_repeats': page_setting.show_repeat, 'theme_list':theme_list, 'selected_theme':user_profile.theme_id}, context_instance=template.RequestContext(request))
  

    
@login_required
def profile(request,form_class=User_ProfileForm, template_name="dashboard/dashboard_user_profile.html"):
    referer = request.META['PATH_INFO']
    if str(referer.split('/')[1])!=str(request.user.username):
        return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/profile/')
    new_data, errors = {}, {}
    user_profile = get_object_or_404(User_Profile, user=int(request.user.id))
    displayname = get_display_name(request.user)
    if len(displayname)>18:
        displayname = displayname[0:14]+'...'
    if user_profile:
        form = User_ProfileForm(instance=user_profile)
    else:
        form = User_ProfileForm()
    fire_eagle = Fireeagle.objects.filter(user=request.user)
    if fire_eagle:
        eagle_integrated = True
    else:
        eagle_integrated = False
    if request.method == "POST":
        
        if not request.FILES:        
            form = User_ProfileForm(request.POST)
        else:        
            form = User_ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            form.save(request)
            request.session['flash'] = "Changes saved"
            # Delete the user profile and user information
            cache_key = '%s_profilequery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,request.user.id,)
            cache.delete(cache_key)
            cache_key = '%s_user%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,request.user.id,)
            cache.delete(cache_key)
        return render_to_response(template_name, {'form': form ,'user_profile': user_profile, 'displayname':displayname, 'eagle_integrated':eagle_integrated,},context_instance=template.RequestContext(request))     
    return render_to_response(template_name, { 'form': form , 'user_profile': user_profile, 'displayname':displayname,'eagle_integrated':eagle_integrated,},context_instance=template.RequestContext(request))     

@login_required
def dashboard(request,form_class=User_ProfileForm):
    return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/import/')

#def twitter_invites_status(data,inv_type):
def twitter_invites_status(data):                                           
    #if inv_type=='Twitter':
    #    invi_type =2
    #elif inv_type =='GTalk':
    #    invi_type =3
    #elif inv_type =='Yahoo':
    #    invi_type = 4
    new_data = []
    registered_list = ''
    for item in data:
        dict = {}
        converted_invite = Invite.objects.filter(invite_type=2, status = 2, invitee_email=str(item['user']))
        if converted_invite:
            converted_invite = converted_invite[0]
            dict['status'] = get_object_or_404(User, id=converted_invite.converted_user_id).username
            registered_list = registered_list + str(dict['status']) + ','
        else:
            converted_invite = Invite.objects.filter(invite_type=2, invitee_email=str(item['user']))
            if converted_invite:
                dict['status'] = 'invited'
            else:
                dict['status'] = ''            
        dict['user'] = item['user']
        dict['image'] = item['image']
        new_data.append(dict)
    return {'new_data': new_data, 'registered_list':registered_list.strip(',')}
                
