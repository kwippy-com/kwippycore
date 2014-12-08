from django.contrib.auth.models import *
from django import template
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.views.generic.simple import redirect_to
from django.conf import settings
from django.template import RequestContext
from kwippy.models.quip import Quip
from kwippy.models.follower import Follower
from kwippy.models.featured_user import Featured_User
from kwippy.models.favourite import Favourite
from kwippy.views.mykwips import details_for_kwips_page
from kwippy.views.main import get_display_name, comment_count, kwip_count, random_users, active_users

def main(request,user_login, quips_for='favourites'):
  quips_for = 'favourites'
  page = int(request.GET.get('page',1)) 
  if request.GET.get('page') and page==0:
    if user_login=='everyone':
      return HttpResponseRedirect('/everyone/favoritekwips/')
    else:
      return HttpResponseRedirect('/'+user_login+'/'+'kwips/') 
  paginate_by = 20
  if user_login != 'everyone':
      login_user = get_object_or_404(User, username=user_login)
      if login_user.is_active == 3:
          raise Http404
      dict = details_for_kwips_page(request,user_login)
      favs = Favourite.objects.filter(user=login_user).order_by('-created_at')[(paginate_by*page):(paginate_by*(page+1))]
      user_favs_count = favs.count()
      user_kwips_count = kwip_count(dict['user'])
      user_comments_count = comment_count(dict['user'])
      random_users_set = None
      active_users_set = None
      page_type = 'favorite'
      quip_ids_in_csv = []
      for fav in favs:
          quip_ids_in_csv.append(int(fav.quip.id))
      quips = Quip.objects.filter(id__in=quip_ids_in_csv).order_by('-created_at')
  else:
      dict = {}
      if request.user.is_authenticated():
        user_login=request.user.username
      else:
        user_login = 'kwippy' 
      favs = Favourite.objects.all().order_by('-created_at')[(paginate_by*page):(paginate_by*(page+1))]
      user_favs_count = None
      user_kwips_count = None
      user_comments_count = None
      random_users_list = random_users(9)
      random_users_set = User.objects.filter(id__in=random_users_list)
      active_users_set = active_users(9)
      page_type = 'everyone'
      quips = favs
  featured_users_set = Featured_User.objects.all().order_by('-id')[:3]
  if quips:    
    paginator = Paginator(quips, paginate_by)
    quips_page = paginator.page(page)
    quips = paginator.object_list
    return render_to_response('myfavorites.html', {'is_paginated': paginator.num_pages > 1, 'results_per_page': paginate_by,
                              'has_next': quips_page.has_next(), 'has_previous': quips_page.has_previous(),
                              'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': 0,
                              'hits' : 0, 'login': user_login,'quips': quips,'random_users':random_users_set,
                              'quips_for': quips_for,'favs_count':user_favs_count,'dict':dict,'active_users':active_users_set,
                              'revision_number': settings.REVISION_NUMBER,'favs_count':user_favs_count,'featured_users':featured_users_set,
                              'kwip_count':user_kwips_count,'page_type':page_type,'comment_count':user_comments_count}, context_instance=template.RequestContext(request))  
  else:
    return render_to_response('myfavorites.html', {'login': user_login,
                              'quips_for': quips_for, 'dict': dict,
                              'revision_number': settings.REVISION_NUMBER,'featured_users':featured_users_set,
                              'kwip_count':user_kwips_count,'page_type':page_type,'comment_count':user_comments_count}, context_instance=template.RequestContext(request))  

