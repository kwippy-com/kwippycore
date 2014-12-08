import os,pdb
from django import template, http
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from kwippy.views.main import get_display_name
from kwippyproject.kwippy.models.page_setting import Page_Setting
from kwippyproject.kwippy.forms.page_setting_form import *

@login_required
def show_hide_repeats(request):
    referer = request.META['PATH_INFO']
    if request.method == "POST":
	form = 

def import_ims(request, template_name = "dashboard/dashboard_import.html"):    
    referer = request.META['PATH_INFO']
    if str(referer.split('/')[1])!=str(request.user.username):
        return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/')
    new_data, errors = {}, {}
    user_profile = get_object_or_404(User_Profile, user=int(request.user.id))
    displayname = get_display_name(request.user)
    return render_to_response('dashboard/dashboard_import.html', { 'displayname':displayname,'user_profile': user_profile,},context_instance=template.RequestContext(request))     
    
@login_required
def profile(request,form_class=User_ProfileForm, template_name="dashboard/dashboard_user_profile.html"):
    referer = request.META['PATH_INFO']
    if str(referer.split('/')[1])!=str(request.user.username):
        return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/')
    new_data, errors = {}, {}
    user_profile = get_object_or_404(User_Profile, user=int(request.user.id))
    displayname = get_display_name(request.user)
    if len(displayname)>18:
        displayname = displayname[0:14]+'...'
    if user_profile:
        form = User_ProfileForm(instance=user_profile)
    else:
        form = User_ProfileForm()
    if request.method == "POST":
        if not request.FILES:        
            form = User_ProfileForm(request.POST)
        else:        
            form = User_ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            form.save(request)
            request.session['flash'] = "Changes saved"             
        return render_to_response(template_name, { 'form': form ,'user_profile': user_profile, 'displayname':displayname},context_instance=template.RequestContext(request))     
    return render_to_response(template_name, { 'form': form , 'user_profile': user_profile, 'displayname':displayname,},context_instance=template.RequestContext(request))     

@login_required
def dashboard(request,form_class=User_ProfileForm):
    return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/import/')

  
