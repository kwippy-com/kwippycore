from django.contrib.auth.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from kwippy.models.friend import Friend
from kwippy.models.follower import Follower
from kwippy.views.main import get_display_name, comment_count, kwip_count
from kwippy.views.comm_queue import send_mail,send_im
from django.core.cache import cache
from django.conf import settings
import pdb


@login_required
def add_friend(request,friendship_offeree):
  if request.META.has_key('HTTP_REFERER'):
    referer = request.META.get('HTTP_REFERER', '')
  else:
    referer = str(request.user.username)  
  friendship_offerer = request.user
  friendship_offeree = get_object_or_404(User, username = friendship_offeree)
  friendship = Friend.objects.filter(sender=friendship_offerer,receiver=friendship_offeree) | Friend.objects.filter(sender=friendship_offeree,receiver=friendship_offerer)
  if not friendship:
    friendship = Friend(sender = friendship_offerer, receiver = friendship_offeree)
    friendship.save()
    params_for_mail = {'#_1':friendship_offeree.username,'#_2':friendship_offerer.username}
    send_mail(str(friendship_offeree.email), 'kwippy <support@kwippy.com>', 'friend_request', params_for_mail)
    send_im(friendship_offeree,'friend_request', params_for_mail)    
  else:
    pending_request = Friend.objects.filter(sender=friendship_offeree,receiver=friendship_offerer, status=0)
    if pending_request:
      pending_request = pending_request[0]
      pending_request.status=1
      pending_request.save()
      if not Follower.objects.filter(follower=friendship_offerer, followee=friendship_offeree):
          follow = Follower(follower=friendship_offerer, followee=friendship_offeree)
          follow.save()
      if not Follower.objects.filter(follower=friendship_offeree, followee=friendship_offerer):
          follow_1 = Follower(follower=friendship_offeree, followee=friendship_offerer)
          follow_1.save()
      params_for_mail = {'#_1':friendship_offeree.username,'#_2':request.user.username}    
      send_mail(str(friendship_offeree.email), 'kwippy <support@kwippy.com>', 'friend_request_accepted', params_for_mail)
      send_im(friendship_offeree,'friend_request_accepted', params_for_mail)
  return HttpResponseRedirect(referer)

@login_required
def remove_friend(request,friendship_offeree):
  if request.META.has_key('HTTP_REFERER'):
    referer = request.META.get('HTTP_REFERER', '')
  else:
    referer = str(request.user.username)    
  user_1 = request.user
  user_2 = get_object_or_404(User, username = friendship_offeree)
  friendship = Friend.objects.filter(sender = user_1, receiver = user_2, status =1) |  Friend.objects.filter(sender = user_2, receiver = user_1, status =1)
  friendship.delete()
  # delete follower relation for the deletion initiator
  follow = Follower.objects.filter(follower=user_1,followee=user_2)
  follow.delete()
  cache_key = '%s_follow%dto%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,user_1.id,user_2.id,)
  cache.delete(cache_key)
  cache_key = '%s_userfollowerquery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,user_2.id,)
  cache.delete(cache_key)
  cache_key = '%s_userfolloweequery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,user_1.id,)
  cache.delete(cache_key)
  cache_key = '%s_followercount%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,user_2.id,)
  cache.delete(cache_key)
  cache_key = '%s_followeecount%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,user_1.id,)
  cache.delete(cache_key)    
  return HttpResponseRedirect(referer)

@login_required
def pending_requests(request):
  loggedin_user = request.user
  pending_requests = Friend.objects.filter(receiver=loggedin_user,status=0)
  return pending_requests

@login_required
def accept_deny_requests(request, offerer_username):
  if request.META.has_key('HTTP_REFERER'):
    referer = request.META.get('HTTP_REFERER', '')
  else:
    referer = str(request.user.username)  
  loggedin_user = request.user
  friendship_offerer = get_object_or_404(User, username = offerer_username)
  requests = Friend.objects.filter(receiver=loggedin_user, sender=friendship_offerer,status=0)
  pending_request = requests[0]
  if request.POST.has_key('accept'):
    pending_request.status = 1
    pending_request.save()
    if not Follower.objects.filter(follower=friendship_offerer,followee=loggedin_user):
      follow = Follower(follower=friendship_offerer,followee=loggedin_user)
      follow.save()
    if not Follower.objects.filter(follower=loggedin_user,followee=friendship_offerer):
      follow_1 = Follower(follower=loggedin_user,followee=friendship_offerer)
      follow_1.save()              
    params_for_mail = {'#_1':friendship_offerer.username,'#_2':request.user.username}    
    send_mail(str(friendship_offerer.email), 'kwippy <support@kwippy.com>', 'friend_request_accepted', params_for_mail)
    send_im(friendship_offerer,'friend_request_accepted', params_for_mail)
  else:
    pending_request.delete()
    # if not following already the sender becomes a follower of receiver
    if not Follower.objects.filter(follower=friendship_offerer,followee=loggedin_user):
      follow = Follower(follower=friendship_offerer,followee=loggedin_user)
      follow.save()      
  return HttpResponseRedirect(referer)

def isfriend(user1, user2):
  friendships = Friend.objects.filter(sender=user1, receiver=user2, status=1) | Friend.objects.filter(sender=user2, receiver=user1, status=1)
  if friendships:
    return True
  else:
    return False
  

