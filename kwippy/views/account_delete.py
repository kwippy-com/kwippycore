from django import template, http
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from kwippy.models.user_profile import User_Profile
#from kwippy.models.invite import Invite
from kwippy.models.account import Account
from kwippy.models.account_delete import AccountDelete
from kwippy.models.follower import Follower
from kwippy.models.friend import Friend
#from kwippy.models.featured_kwip import Featured_Kwip
from django.contrib.auth.models import User
from django.db import connection

@login_required
def main(request,user_login):   
  if request.user.is_authenticated():
    # set is_active = 3, give 404 for kwips pages,comments page, favs page, delete followers,followees
    user = get_object_or_404(User, id=request.user.id)
    if user.username == user_login:
      cursor = connection.cursor()
      cursor.execute("update auth_user set is_active=3 where id= %d" %int(user.id))
      cursor.close()
      #user.is_active = 3
      #user.save()
      acc_de = AccountDelete.objects.filter(user=user)
      if not acc_de:
        acc_del = AccountDelete(user=user)
        acc_del.save()
      # delete followers, followees & friends
      followers = Follower.objects.filter(followee=user)
      followers.delete()
      followees = Follower.objects.filter(follower=user)
      followees.delete()
      friend_sender = Friend.objects.filter(sender=user)
      friend_sender.delete()
      friend_receiver = Friend.objects.filter(receiver=user)
      friend_receiver.delete()
      # mark media_processed=0
      profile = get_object_or_404(User_Profile, user=user)
      profile.media_processed = 0
      profile.save()
      # disable accounts
      accounts = Account.objects.filter(user=user)
      for acc in accounts:
        acc.status = 3 # inactive
        acc.save()
      logout(request)
    return HttpResponseRedirect('/')  
   
