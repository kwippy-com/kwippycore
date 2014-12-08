from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from kwippy.models.follower import Follower
from kwippy.models.friend import Friend
from kwippy.views.comm_queue import send_mail,send_im
from django.core.cache import cache
from django.conf import settings

@login_required
def im_notification(request,followee_username):
  followee_user = get_object_or_404(User, username=followee_username)
  if request.META.has_key('HTTP_REFERER'):
    referer = request.META.get('HTTP_REFERER', '')
  else:
    referer = str(followee_username)  
  follower_user = get_object_or_404(User,id=request.user.id)
  if follower_user!=followee_user and request.POST.has_key('im_notifications'):
    follow = get_object_or_404(Follower, followee=followee_user, follower=follower_user)
    follow.im_notification = int(request.POST['im_notifications'])
    follow.save()
    friendship = Friend.objects.filter(sender = followee_user, receiver = follower_user) | Friend.objects.filter(sender = follower_user, receiver = followee_user)
    if friendship:
      if int(request.POST['are_friends']) == 0:
        friendship[0].delete()
      else:
        friendship[0].status = 1
        friendship[0].save()
    else:
      if int(request.POST['are_friends']) == 1:
        fship = Friend(sender=follower_user, receiver=followee_user)
        fship.save()
        if not Follower.objects.filter(follower=follower_user,followee=followee_user): 
          follow_1 = Follower(follower=follower_user,followee=followee_user)
          follow_1.save()
          cache_key = '%s_follow%dto%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,follower_user.id,followee_user.id,)
          cache.delete(cache_key)
          cache_key = '%s_userfollowerquery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,followee_user.id,)
          cache.delete(cache_key)
          cache_key = '%s_userfolloweequery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,follower_user.id,)
          cache.delete(cache_key)
          cache_key = '%s_followercount%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,followee_user.id,)
          cache.delete(cache_key)
          cache_key = '%s_followeecount%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,follower_user.id,)
          cache.delete(cache_key)    
        params_for_mail = {'#_1':followee_user.username,'#_2':follower_user.username}
        send_mail(str(followee_user.email), 'kwippy <support@kwippy.com>', 'friend_request', params_for_mail)
        send_im(followee_user,'friend_request', params_for_mail)
    request.session['flash'] = "settings saved" 
  return HttpResponseRedirect(referer)


