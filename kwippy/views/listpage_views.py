from django.db import connection
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import *
from django import template, http
from kwippy.views.main import get_display_name
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from kwippyproject.kwippy.models.user_profile import User_Profile
from django.core.paginator import Paginator

def queryset_to_csv(queryset,type):
  csv = []
  for q in queryset:
    if type=='followers':
      csv.append(int(q.follower.id))
    else:
      csv.append(int(q.followee.id))
  return csv  

@login_required
def myfollowers(request,user_login):
    if user_login!='kwippy':
      paginate_by = 20
      user = get_object_or_404(User, username=user_login)
      displayname = get_display_name(user)
      user_profile = user.get_profile()    
      if request.user.is_authenticated():
        logged_in_user_profile = request.user.get_profile()
      else:
        logged_in_user_profile = False
      followers = user.followee.all().order_by('-created_at')
      followers_list_in_csv = queryset_to_csv(followers,'followers')        
      followers_profiles = User_Profile.objects.filter(user__in=followers_list_in_csv)      
      paginator = Paginator(followers_profiles, paginate_by)
      page = int(request.GET.get('page',1)) 
      fp_page = paginator.page(page)
      fp = fp_page.object_list
      return render_to_response('list_pages/followees_followers.html', {'is_paginated': paginator.num_pages > 1, 'results_per_page': paginate_by,
                              'has_next': fp_page.has_next(), 'has_previous': fp_page.has_previous(),
                              'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': 0,
                              'hits' : 0,'followers_profiles':fp,
                              'type':'followers','logged_in_user_profile':logged_in_user_profile, 'displayname':displayname,
                              'user_profile':user_profile,}, context_instance=template.RequestContext(request))
    else:
      return HttpResponseRedirect('/kwippy/')

@login_required
def myfriends(request,user_login):
    cursor = connection.cursor()
    if user_login!='kwippy':
      paginate_by = 20
      user = get_object_or_404(User, username=user_login)
      displayname = get_display_name(user)
      user_profile = user.get_profile()    
      if request.user.is_authenticated():
        logged_in_user_profile = request.user.get_profile()
      else:
        logged_in_user_profile = False
      cursor.execute('select sender_id from kwippy_friend where receiver_id=%s and status=1 union select receiver_id from kwippy_friend where sender_id=%s and status=1',(user.id,user.id,))
      user_ids = [item[0] for item in cursor.fetchall()]
      friends_profiles = User_Profile.objects.filter(user__in=user_ids)      
      paginator = Paginator(friends_profiles, paginate_by)
      page = int(request.GET.get('page',1)) 
      fp_page = paginator.page(page)
      fp = fp_page.object_list
      return render_to_response('list_pages/friends_list.html', {'is_paginated': paginator.num_pages > 1, 'results_per_page': paginate_by,
                              'has_next': fp_page.has_next(), 'has_previous': fp_page.has_previous(),
                              'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': 0,
                              'hits' : 0,'friends_profiles':fp,
                              'logged_in_user_profile':logged_in_user_profile,
                              'user_profile':user_profile,}, context_instance=template.RequestContext(request))
    else:
      return HttpResponseRedirect('/kwippy/')


@login_required
def myfollowees(request,user_login):
    paginate_by = 20
    user = get_object_or_404(User, username=user_login)
    user_profile = user.get_profile()
    displayname = get_display_name(user)
    if request.user.is_authenticated():
      logged_in_user_profile = request.user.get_profile()
    else:
      logged_in_user_profile = False
    followees = user.follower.all().order_by('-created_at')
    followees_list_in_csv = queryset_to_csv(followees,'followees')
    followees_profiles = User_Profile.objects.filter(user__in=followees_list_in_csv)      
    paginator = Paginator(followees_profiles, paginate_by)
    page = int(request.GET.get('page',1)) 
    fp_page = paginator.page(page)
    fp = fp_page.object_list
    return render_to_response('list_pages/followees_followers.html', {'is_paginated': paginator.num_pages > 1, 'results_per_page': paginate_by,
                              'has_next': fp_page.has_next(), 'has_previous': fp_page.has_previous(),
                              'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': 0,
                              'hits' : 0,'followers_profiles':fp,
                             'type':'followees','logged_in_user_profile':logged_in_user_profile, 'displayname': displayname,
                             'user_profile':user_profile,}, context_instance=template.RequestContext(request))
