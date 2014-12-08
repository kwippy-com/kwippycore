from kwippyproject.kwippy.forms.auth_forms import AuthenticationForm, PasswordResetForm, PasswordChangeForm, ForgotPasswordForm
from django import forms
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext, loader, Context
from django.contrib.sites.models import Site, RequestSite
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.translation import ugettext as _
from django.contrib.auth.models import *
from django.contrib.auth.decorators import login_required
from kwippy.views.mykwips import follow_user_nomail
from kwippyproject.kwippy.models.forgot_password import ForgotPassword
import pdb


def login(request, template_name='signup/twitter.html', redirect_field_name=REDIRECT_FIELD_NAME):
    "Displays the login form and handles the login action for twitters."
    if request.user.is_authenticated():
	request.session['flash']='already logged in as \"'+request.user.username+'\" , to login as someone else plz logout first.'
	return HttpResponseRedirect('/'+request.user.username+'/')	
    manipulator = AuthenticationForm(request)
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    if request.POST:        
        errors = manipulator.get_validation_errors(request.POST)
        if not errors:
	    email=request.POST['email']
	    user=User.objects.filter(email=email)
	    if user:
		request.session['last_login'] = user[0].last_login
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                from django.conf import settings
                redirect_to = settings.LOGIN_REDIRECT_URL
            from django.contrib.auth import login
	    if is_first_login(request.POST['email']):
		login(request, manipulator.get_user())
		request.session.delete_test_cookie()
		request.session['first_login'] = True
		return HttpResponseRedirect('/'+manipulator.get_user().username+'/dashboard')
	    else:				
		if len(request.POST) == 4 and request.POST['Remember']:	
		    request.session[settings.PERSISTENT_SESSION_KEY] = True
		login(request, manipulator.get_user())
		request.session.delete_test_cookie()
		request.session['first_login'] = False		
		if not redirect_to or redirect_to=='/accounts/profile/':
		    return HttpResponseRedirect('/'+manipulator.get_user().username+'/')
		else:
		    return HttpResponseRedirect(redirect_to)
    else:
        errors = {}
    request.session.set_test_cookie()

    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)

    return render_to_response(template_name, {
        'form': oldforms.FormWrapper(manipulator, request.POST, errors),
        redirect_field_name: redirect_to,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))

def logout(request, next_page=None, template_name='signup/logged_out.html'):
    "Logs out the user and displays 'You are logged out' message."
    from django.contrib.auth import logout
    logout(request)
    request.session[settings.PERSISTENT_SESSION_KEY] = False
    if next_page is None:
	return HttpResponseRedirect('/login/')
        #return render_to_response(template_name, {'title': _('Logged out')}, context_instance=RequestContext(request))
    else:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page or request.path)


def is_first_login(email):
    #pdb.set_trace()
    user = User.objects.filter(email=email)
    if user:
        user=user[0]
	if user.last_login!=user.date_joined:
	    return False
	else:
	    return True
    else:
        user = User.objects.filter(username=email)
        if user:
            user=user[0]
            if user.last_login!=user.date_joined:
                return False
            else:
                return True

        


