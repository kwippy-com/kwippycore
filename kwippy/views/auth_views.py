from kwippyproject.kwippy.forms.auth_forms import AuthenticationForm, PasswordChangeForm, ForgotPasswordForm, PasswordResetForm
from django import forms
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader, Context
from django.contrib.sites.models import Site, RequestSite
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.translation import ugettext as _
from django.contrib.auth.models import *
from django.contrib.auth.decorators import login_required
from kwippy.views.mykwips import follow_user_nomail
from kwippyproject.kwippy.models.forgot_password import ForgotPassword
from kwippy.views.comm_queue import send_mail
from signup_app.models import SignupProfile
import sha,random,os

def login(request, template_name='signup/login.html',redirect_field_name=REDIRECT_FIELD_NAME):
    if request.user.is_authenticated():
        request.session['flash']='already logged in as \"'+request.user.username+'\" , to login as someone else plz logout first.'
        return HttpResponseRedirect('/'+request.user.username+'/')
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.POST:
        #if request.session.test_cookie_worked():
            #request.session.delete_test_cookie()
        #else:
            #return HttpResponseRedirect('/login')
        loginform = AuthenticationForm(request.POST)
        isfirst_login = is_first_login(request.POST['email'])
        if loginform.login(request):
            if request.POST.has_key('Remember'):
                request.session[settings.PERSISTENT_SESSION_KEY] = True
            if isfirst_login:
                request.session['first_login'] = True
                url_to = '/'+loginform.user.username+'/dashboard/invite/?type=1login'
	    elif not redirect_to or redirect_to=='/accounts/profile/':
                request.session['first_login'] = False
                url_to = '/'+loginform.user.username+'/active/'
            else:
                request.session['first_login'] = False
                url_to = redirect_to
            return HttpResponseRedirect(url_to)
    else:
        #request.session.set_test_cookie()
        loginform = AuthenticationForm()

    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
	
    return render_to_response(template_name, {
        'form': loginform,
        redirect_field_name: redirect_to,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))

def logout(request, next_page=None, template_name='signup/logged_out.html'):
    "Logs out the user and displays 'You are logged out' message."
    from django.contrib.auth import logout
    logout(request)
    try:
        request.session[settings.PERSISTENT_SESSION_KEY] = False
    except AttributeError:
        print "Logout conked"
    if next_page is None:
	return HttpResponseRedirect('/login/')
        #return render_to_response(template_name, {'title': _('Logged out')}, context_instance=RequestContext(request))
    else:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page or request.path)

def password_change(request, template_name='signup/password_change_form.html'):
    new_data, errors = {}, {}
    form = PasswordReset(request.user)
    if request.POST:
        new_data = request.POST.copy()
        errors = form.get_validation_errors(new_data)
        if not errors:
            form.save(new_data)
            return HttpResponseRedirect('%sdone/' % request.path)
    return render_to_response(template_name, {'form': PasswordReset()},context_instance=RequestContext(request))
    password_change = login_required(password_change)
    
def reset_password(request, reset_link, template_name='signup/forgot_password_form.html'):
    new_data, errors = {}, {}
    if reset_link:
        usr_fgt_pwd = get_object_or_404(ForgotPassword, reset_link=reset_link)

        if not usr_fgt_pwd.is_active:
            usr_fgt_pwd.delete()
            request.session['flash']='This link has expired.'	    
            return HttpResponseRedirect('/home/forgotpassword/')
        
        user = usr_fgt_pwd.user
        form = ForgotPasswordForm()
        if request.method == "POST":
            form = ForgotPasswordForm(request.POST)
            if form.is_valid():
                form.save(user)
                if not user.is_active:
                    activation_key = get_object_or_404(SignupProfile, user=user).activation_key
                    account = SignupProfile.objects.activate_user(activation_key)
                usr_fgt_pwd.is_active = 0
                usr_fgt_pwd.save()
		request.session['flash']='Password changed successfully. You may login.'	    
                url_to = '/login/?'+user.username
                return HttpResponseRedirect(url_to)
        return render_to_response(template_name, {'form': form },context_instance=RequestContext(request))        
    
def forgot_password(request, is_admin_site=False, template_name='signup/password_reset_form.html'):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.get(email=email)

            if email and user:
                reset_link = sha.new(user.email+str(random.random())).hexdigest()[:20]
                f=ForgotPassword(user=user,reset_link=reset_link)
                f.save()
                params_for_mail = {'#_1':user.username,'#_2':str(reset_link)}
                send_mail(str(email),'kwippy <support@kwippy.com>','forgot_password',params_for_mail)                            
              	request.session['flash']='the \"reset password\" link has been sent to \"'+str(request.POST['email'])+'".'
                url_to = '/login/?'+user.username          	
        	return HttpResponseRedirect(url_to)
        else:
            request.session['flash']='There\'s no user with the e-mail \"'+str(request.POST['email'])+'".'
            return HttpResponseRedirect('/home/forgotpassword/')

    else:
        form = PasswordResetForm()
        
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))

def password_reset_done(request, template_name='signup/password_reset_done.html'):
    return render_to_response(template_name, context_instance=RequestContext(request))


def is_first_login(email):
    user = User.objects.filter(email=email)
    if user:
        user=user[0]
	if user.last_login ==user.date_joined:
	    return True
        else:
            return False
            
    else:
        user = User.objects.filter(username=email)
        if user:
            user=user[0]
            if user.last_login == user.date_joined:
                return True
            else:
                return False
