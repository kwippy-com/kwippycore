"""
Views which allow users to create and activate accounts.

"""

import pdb,os,random,sha
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext,Context, loader
from django.contrib.auth.models import *
from kwippy.views.main import get_display_name
from signup_app.forms import SignupForm, SignupFormUniqueEmail 
from signup_app.models import SignupProfile
from kwippyproject.kwippy.models.user_profile import User_Profile
from kwippyproject.kwippy.models.page_setting import PageSetting
from kwippyproject.kwippy.models.notification_setting import NotificationSetting
from kwippy.models.invite import Invite
from kwippy.models.invite_limit import Invite_Limit
from kwippyproject.kwippy.views.comm_queue import send_mail
from kwippy.views.mykwips import follow_user_nomail
from django.http import Http404

def activate(request, activation_key, template_name='signup/activate.html'):
    """
    Activates a ``User``'s account, if their key is valid and hasn't
    expired.
    
    By default, uses the template ``signup/activate.html``; to
    change this, pass the name of a template as the keyword argument
    ``template_name``.
    
    Context:
    
        account
            The ``User`` object corresponding to the account, if the
            activation was successful. ``False`` if the activation was
            not successful.
    
        expiration_days
            The number of days for which activation keys stay valid
            after signup.
    
    Template:
    
        signup/activate.html or ``template_name`` keyword
        argument.
    
    """    
    activation_key = activation_key.lower() # Normalize before trying anything with it.
    account = SignupProfile.objects.activate_user(activation_key)
    if account:
        url_to = '/login/?'+account.username
    else:
        url_to = '/login/'
    request.session['flash']='cool, your account has been activated.'	
    return HttpResponseRedirect(url_to)

def signup(request, invitation_hash, success_url='/accounts/signup/complete/',
             form_class=SignupFormUniqueEmail, profile_callback=None,
             template_name='signup/signup_form_new.html'):
    """
    Allows a new user to register an account.
    
    Following successful signup, redirects to either
    ``/accounts/signup/complete/`` or, if supplied, the URL
    specified in the keyword argument ``success_url``.
    
    By default, ``signup_app.forms.SignupForm`` will be used
    as the signup form; to change this, pass a different form
    class as the ``form_class`` keyword argument. The form class you
    specify must have a method ``save`` which will create and return
    the new ``User``, and that method must accept the keyword argument
    ``profile_callback`` (see below).
    
    To enable creation of a site-specific user profile object for the
    new user, pass a function which will create the profile object as
    the keyword argument ``profile_callback``. See
    ``SignupManager.create_inactive_user`` in the file
    ``models.py`` for details on how to write this function.
    
    By default, uses the template
    ``signup/signup_form.html``; to change this, pass the
    name of a template as the keyword argument ``template_name``.
    
    Context:
    
        form
            The signup form.
    
    Template:
    
        signup/signup_form.html or ``template_name``
        keyword argument.
    
    """
#    commented to test the new signup page    
#    if request.user.is_authenticated():
#	return HttpResponseRedirect('/'+request.user.username+'/')	
    
    if request.method == 'POST':
        form = SignupFormUniqueEmail(request.POST)
        if form.is_valid():
            # passing the invitation_hash to be stored in signup_profile
            # for cases where signup is from invitation links
            if invitation_hash:
                new_user = form.save(invitation_hash,profile_callback=profile_callback)
            else:
                new_user = form.save(profile_callback=profile_callback)
            user = get_object_or_404(User, username=new_user.username)
            #os.system("htpasswd -b "+settings.AUTH_FILE+" "+user.username+" "+ form.cleaned_data['password1'])
            if user:
		signup_key = SignupProfile.objects.filter(user=int(user.id))
            if signup_key:
                signup_key=signup_key[0].activation_key
	    ''' the code below will create a profile for the new user and 
	     associate a random hash with it, create a default page_setting, create a default notification_setting 
	     and set his display_name as his url display name can obviously by edited via dashboard '''
	    if user.email:
		random_hash = sha.new(str(user.email)+str(random.random())).hexdigest()[:10]
		user_profile = User_Profile(user=user,display_name=user.username,hash=random_hash,quip_repeat_total=1,quip_total=1)
		user_profile.save()
		page_setting = PageSetting(user=user)
		page_setting.save()
		not_setting = NotificationSetting(user=user)
		not_setting.save()
	    #adding default followee
	    invite = Invite.objects.filter(unique_hash=invitation_hash)
	    #getting all the invites sent to this email id
            all_invites=Invite.objects.filter(invitee_email=str(invite[0].invitee_email))
            if all_invites:
                for inv in all_invites:
                    # everyone who invited the new person becomes their default follower
                    # and the new user too follows them all back :D.
                    invitee=get_object_or_404(User, id=inv.user_id)
                    #follow_user_nomail(invitee,user.username,0)
                    follow_user_nomail(user,invitee.username,1)
	    #adding kwippy as default followee
	    follow_user_nomail(user,'kwippy',1)
            # call to comm_queue
            send_mail(str(user.email),'support@kwippy.com','account_activation',{'#_1':user.username,'#_2':signup_key})
            # will make a centralized function to prepare such params as above
            request.session['flash']='Thanks for signing up '+user.username+ '!! An activation email has been sent to '+'"'+str(user.email)+'"'
	    url_to = '/login/?'+user.username
	    return HttpResponseRedirect(url_to)
        else:
	    request.session['flash']='Please fill all the fields correctly.'	    
	return render_to_response(template_name,
                              { 'form': form },
                              context_instance=RequestContext(request))	
    else:
       #code to check whether the invite code is valid and active(status 0 i.e)
        invite = get_object_or_404(Invite, unique_hash=invitation_hash)
        invite_limit = Invite_Limit.objects.filter(invite=invite)
        allow = invite.status
        if len(invite_limit)==1:
            invite_limit = invite_limit[0]
            if invite_limit.count>invite_limit.maxcount:
                raise Http404
            allow = 0
        if invite and allow==0:
            form = form_class()
	    #redirecting admins to diff signup page
	    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=RequestContext(request))
	else:
	    request.session['flash']='Oops this invite has been used. Submit your email id below for another invite.' 
	    url_to = '/signup/?'+invitation_hash
	    return HttpResponseRedirect(url_to)

