from django.contrib.auth.models import *
from django import template, http
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic.simple import direct_to_template, redirect_to
from django.conf import settings
from django.template import RequestContext
from django.db import connection
from django.core.paginator import Paginator
from kwippy.models.quip import Quip
from kwippy.models.account import Account
from django.contrib.comments.models import Comment
from kwippy.models.favourite import Favourite
from kwippy.models.featured_user import Featured_User
from kwippy.views.views import queryset_to_csv
from kwippy.views.mykwips import details_for_kwips_page
from kwippy.views.main import comment_count, kwip_count, random_users, active_users
from kwippy.views.comm_queue import send_mail


def main(request,user_login, quips_for='favourites'):
  quips_for = 'favourites'
  page = int(request.GET.get('page',1)) 
  paginate_by = 20
  login_user = get_object_or_404(User, username=user_login)
  if login_user.is_active == 3:
    raise Http404
  dict = details_for_kwips_page(request,user_login)
  comments = Comment.objects.filter(user=login_user).order_by('-submit_date')[:100]
  comment_count = comments.count()
  page_type = 'comments'
  quip_ids_in_csv = []
 # for fav in favs:
 #   quip_ids_in_csv.append(int(fav.quip.id))
 # quips = Quip.objects.filter(id__in=quip_ids_in_csv).order_by('-created_at')
  if comments:    
    paginator = Paginator(comments, paginate_by)    
    comments_page = paginator.page(page)
    comments = comments_page.object_list
    return render_to_response('mycomments.html', {'is_paginated': paginator.num_pages > 1, 'results_per_page': paginate_by,
                              'has_next': comments_page.has_next(), 'has_previous': comments_page.has_previous(),
                              'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': 0,
                              'hits' : 0, 'login': user_login,'comments': comments,
                              'quips_for': quips_for,'comment_count':comment_count,'dict':dict,
                              'revision_number': settings.REVISION_NUMBER,
                              'kwip_count':kwip_count(dict['user']),'page_type':page_type,}, context_instance=template.RequestContext(request))  
  else:
    return render_to_response('mycomments.html', {'login': user_login,
                              'quips_for': quips_for,
                              'revision_number': settings.REVISION_NUMBER,'dict':dict,
                              'kwip_count':kwip_count(dict['user']),'page_type':page_type,'comment_count':comment_count}, context_instance=template.RequestContext(request))  


def everyones_comments(request, quips_for='favourites'):
  quips_for = 'favourites'
  page = int(request.GET.get('page',1)) 
  paginate_by = 20
  link = '/everyone/comments/'
  random_users_list = random_users(9)
  random_users_set = User.objects.filter(id__in=random_users_list)
  active_users_set = active_users(9)
  if request.user.is_authenticated():
    user_login=request.user.username
  else:
    user_login = 'kwippy' 
  dict = details_for_kwips_page(request,user_login)
  user = User.objects.get(username = 'kwippy')
  comments = Comment.objects.all().exclude(user=user).order_by('-submit_date')[:100]
  page_type = 'everyone'
  featured_users_set = Featured_User.objects.all().order_by('-id')[:3]
  if comments:    
    paginator = Paginator(comments, paginate_by)    
    comments_page = paginator.page(page)
    comments = comments_page.object_list
    return render_to_response('mycomments.html', {'is_paginated': paginator.num_pages > 1, 'results_per_page': paginate_by,
                              'has_next': comments_page.has_next(), 'has_previous': comments_page.has_previous(),
                              'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': 0,
                              'hits' : 0, 'login': user_login,'comments': comments,
                              'quips_for': quips_for,'active_users':active_users_set,'featured_users':featured_users_set,
                              'revision_number': settings.REVISION_NUMBER,'random_users':random_users_set,
                              'page_type':page_type,}, context_instance=template.RequestContext(request))  
  else:
    return render_to_response('mycomments.html', {'login': user_login,
                              'quips_for': quips_for,
                              'revision_number': settings.REVISION_NUMBER,'dict':dict,'featured_users':featured_users_set,
                              'kwip_count':kwip_count(dict['user']),'page_type':page_type,'comment_count':comment_count}, context_instance=template.RequestContext(request))  

