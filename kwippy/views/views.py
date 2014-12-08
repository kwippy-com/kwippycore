import random, pdb, datetime
from django import template, http
from kwippy.views.comm_queue import send_mail_old
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from kwippy.models.quip import Quip
from kwippy.models.invite import Invite
from kwippy.models.feedback import Feedback
from kwippy.models.featured_kwip import Featured_Kwip
from django.contrib.auth.models import User
#from kwippyproject.kwippy.views.feedback_view import fb_question_for_page

def home(request):   
  if request.user.is_authenticated():
    return HttpResponseRedirect('/'+str(request.user.username)+'/')  
  else:
    featured_kwips = Featured_Kwip.objects.all().order_by('-created_at')[:1][0]
    return render_to_response('static_pages/home.html',{'featured_kwips': featured_kwips})
   
def isvaliduser(text):
  user = User.objects.filter(username=text)
  if user:
    return True
  else:
    return False

@login_required  
def dashboard(request):   
  if request.user.is_authenticated():
    return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/')    

@login_required
def dashboard_profile(request):   
  if request.user.is_authenticated():
    return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/profile/')

@login_required
def dashboard_invite(request):   
  if request.user.is_authenticated():
    return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/invite/')    


@login_required  
def dashboard_account(request):   
  if request.user.is_authenticated():
    return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/account/')

@login_required  
def dashboard_kwips_page(request):   
  if request.user.is_authenticated():
    return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/kwips_page/')      

def queryset_to_csv(queryset, queryset_type):
  #for sql queries return instead of arrays
  if queryset_type == 'account_forsql':
    csv = ''
  else:
    csv = []
  if queryset_type == "followee":    
    for item in queryset:
      csv.append(int(item.followee.id))
    return csv
  elif queryset_type == "follower":
    for item in queryset:      
      csv.append(int(item.follower.id))
    return csv
  elif queryset_type == "comment_follower":
    for item in queryset:      
      csv.append(int(item.user.id))
    return csv 
  elif queryset_type == "account":    
    for item in queryset:
      csv.append(int(item.id))      
    return csv  
  elif queryset_type == "account_forsql":
    for item in queryset:
      csv = csv + str(item.id) + ','
    return csv.strip(',')
 
@login_required
def store_feedback(request):
  if request.method == "POST":
    referer = request.META.get('HTTP_REFERER', '')
    user = get_object_or_404(User, username=request.user)    
    feedback = Feedback(user=user, page='mykwips', text=request.POST['feedback_box'])    
    feedback.save()
    send_mail_old('feedback@kwippy.com', 'Kwippy <support@kwippy.com>',
                  str(user.username)+'\'s feedback', 'feedback', str(request.POST['feedback_box'])) 
    request.session['flash'] = "Thanks for sharing your feedback." 
  return HttpResponseRedirect(referer)
