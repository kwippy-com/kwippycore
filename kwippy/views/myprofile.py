from django import template
from django.conf import settings
from django.contrib.auth.models import *
from django.template import RequestContext
from django.http import HttpResponseRedirect,Http404
from django.contrib.comments.models import Comment
from django.views.generic.simple import redirect_to
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404

from kwippy.models.quip import Quip
from kwippy.models.account import Account
from kwippy.models.favourite import Favourite
from kwippy.views.mykwips import details_for_kwips_page
from kwippy.views.main import get_display_name, comment_count, kwip_count, favorite_count
import pdb


def main(request,user_login):
  if user_login == 'kwippy':
      return HttpResponseRedirect('/kwippy/') 
  else:
      login_user = get_object_or_404(User, username = user_login)
      if login_user.is_active == 3:
          raise Http404
      dict = details_for_kwips_page(request,user_login)
      accounts = Account.objects.filter(user = login_user)
      recent_kwips = Quip.objects.filter(account__in = accounts).order_by('-created_at')[:3]
      recent_comments = Comment.objects.filter(user = login_user).order_by('-submit_date')[:3]
      recent_favorites = Favourite.objects.filter(user = login_user).order_by('-created_at')[:3]
      recent_activity = {'kwips':recent_kwips, 'comments':recent_comments, 'favorites':recent_favorites}
      return render_to_response('myprofile.html', {'login': user_login,'dict':dict,'recent_activity':recent_activity,
                                                'comment_count':comment_count(login_user),'kwip_count':kwip_count(login_user),'favorite_count':favorite_count(login_user),
                                'revision_number':settings.REVISION_NUMBER}, context_instance=template.RequestContext(request))  
