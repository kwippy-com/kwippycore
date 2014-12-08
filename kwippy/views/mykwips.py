from django.contrib.auth.models import *
from django import template, http
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.views.generic.simple import direct_to_template, redirect_to
from django.conf import settings
from django.template import RequestContext
from django.db import connection
from django.core.cache import *
from kwippy.models.quip import Quip
from kwippy.models.invite import Invite
from kwippy.models.account import Account
from kwippy.models.fireeagle import Fireeagle
from kwippy.models.featured_kwip import Featured_Kwip
from kwippy.models.comment_follower import Comment_Follower
from django.contrib.comments.models import Comment
from kwippy.models.friend import Friend
from kwippy.models.follower import Follower
from kwippy.models.featured_user import Featured_User
from kwippy.models.anon_conversation_invite import Anon_Conversation_Invite
from kwippy.models.favourite import Favourite
from kwippy.models.page_setting import PageSetting
from kwippy.models.user_profile import User_Profile
from kwippy.views.views import queryset_to_csv
from kwippy.views.friend import pending_requests, isfriend
from kwippy.views.main import get_display_name, comment_count, kwip_count, random_users, active_users, rss_users
from kwippy.views.comm_queue import send_mail,send_im
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.db import connection
from django.http import Http404
import oauth
import fireeagle_api
from django.core.paginator import Paginator

CACHE_EXPIRES = 60 * 60 # Expire all the crap in 1 hour

def firee(user):
  if user.is_authenticated():
      fe = Fireeagle.objects.filter(user=user,integrated=1)
      if fe:
          return 1
  return 0

def has_followers(user):
    followers = Follower.objects.filter(followee=user).count()
    if followers:
        return True
    else:
        return False
    
def isfollowing(follower,followee):
  f = Follower.objects.filter(follower=follower,followee=followee)
  if f:
    return True
  else:
    return False

# we can return IM notifications from  here instead of just true or false

def arefriends(user_1,user_2):
  friendship = Friend.objects.filter(sender=user_1, receiver=user_2) | Friend.objects.filter(sender=user_2, receiver=user_1)
  if friendship:
    friendship = friendship[0]
    if friendship.status == 1:
      return 1
    else:
      if Friend.objects.filter(sender=user_1, receiver=user_2):
        return 0
      else:
        return -1 
  else:
    return -1 


def details_for_kwips_page(request,user_login):
  cursor = connection.cursor()
  user = get_object_or_404(User, username=user_login)
  if request.user.is_authenticated():
    logged_in_user_profile = User_Profile.objects.get(user=request.user.id)
  else:
    logged_in_user_profile = False
  if request.user.is_authenticated():
    is_following = isfollowing(request.user,user)
    are_friends = arefriends(request.user,user)
    if is_following:
      is_following_on_im = get_object_or_404(Follower, follower=request.user,followee=user).im_notification
    else:
      is_following_on_im = False
    cache_key = '%s_follow%dto%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,user.id,request.user.id,)
    is_receiver_following = cache.get(cache_key)
    if is_receiver_following is None:
        is_receiver_following = isfollowing(user,request.user)
        cache.set(cache_key,is_receiver_following,CACHE_EXPIRES)
  else:
    is_following_on_im = False 
    is_following = False
    is_receiver_following = False
    are_friends = False  
  
  cache_key = '%s_profilequery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,user.id,)
  user_profile = cache.get(cache_key)
  if user_profile is None:
    user_profile = get_object_or_404(User_Profile, user=user)
    #user_profile = User_Profile.objects.filter(user=user.id)
    cache.set(cache_key, user_profile, CACHE_EXPIRES)
  profile_for_display = {'gender':user_profile.get_gender_display(), 'relationship': user_profile.get_relationship_status_display(), 'birth_month':user_profile.get_birth_month_display()}
  
  cache_key = '%s_userfollowerquery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,user.id,)
  users_followers = cache.get(cache_key)
  if users_followers is None:
    cursor.execute("select auth_user.id from auth_user,kwippy_follower where kwippy_follower.follower_id=auth_user.id and kwippy_follower.followee_id=%s \
    and auth_user.id not in (select receiver_id from kwippy_friend where sender_id=%s and status=1 union \
    select sender_id from kwippy_friend where receiver_id=%s and status=1 )order by auth_user.last_login desc limit 24",(user.id,user.id,user.id,))
    followers_ids = [item[0] for item in cursor.fetchall()]
    users_followers = User.objects.filter(id__in=followers_ids).order_by('-last_login')
    cache.set(cache_key,users_followers,CACHE_EXPIRES)
  
  cache_key = '%s_followercount%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,user.id,)
  followers_count = cache.get(cache_key)
  if followers_count is None:
    cursor.execute('select count(*) from kwippy_follower where followee_id=%s and follower_id not in (select receiver_id from kwippy_friend where sender_id=%s and status=1 union \
    select sender_id from kwippy_friend where receiver_id=%s and status=1)',(user.id,user.id,user.id,))
    (followers_count,)=cursor.fetchone()
    cache.set(cache_key,followers_count,CACHE_EXPIRES)

  #cursor.execute("select id from kwippy_friend where status=1 and (sender_id=%s or receiver_id=%s )",(user.id,user.id,))
  #friend_ids = [item[0] for item in cursor.fetchall()]
  user_frenz = Friend.objects.filter(sender=user, status=1) | Friend.objects.filter(receiver=user, status=1)
  friend_ids = []
  for item in user_frenz:
    if item.sender == user:
      friend_ids.append(int(item.receiver.id))
    else:
      friend_ids.append(int(item.sender.id))
  friends_count = User.objects.filter(id__in=friend_ids).count()
  users_friends = User.objects.filter(id__in=friend_ids).order_by('-last_login')[:9]    

  cache_key = '%s_userfolloweequery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,user.id,)
  users_followees = cache.get(cache_key)
  if users_followees is None:
    cursor.execute("select auth_user.id from auth_user,kwippy_follower where kwippy_follower.followee_id=auth_user.id and kwippy_follower.follower_id=%s \
    and auth_user.id not in (select receiver_id from kwippy_friend where sender_id=%s and status=1 union \
    select sender_id from kwippy_friend where receiver_id=%s and status=1 )order by auth_user.last_login desc limit 9",(user.id,user.id,user.id,))
    followees_ids = [item[0] for item in cursor.fetchall()]
    users_followees = User.objects.filter(id__in=followees_ids).order_by('-last_login')
    cache.set(cache_key,users_followees,CACHE_EXPIRES)
  
  cache_key = '%s_followeecount%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,user.id,)
  followees_count = cache.get(cache_key)
  if followees_count is None:
    cursor.execute('select count(*) from kwippy_follower where follower_id=%s and followee_id not in (select receiver_id from kwippy_friend where sender_id=%s and status=1 union \
    select sender_id from kwippy_friend where receiver_id=%s and status=1 )',(user.id,user.id,user.id,))
    (followees_count,)=cursor.fetchone()
    cache.set(cache_key,followees_count,CACHE_EXPIRES)
  
  cache_key = '%s_favcount%d' %(settings.CACHE_MIDDLEWARE_KEY_PREFIX,user.id,)
  favs_count = cache.get(cache_key)
  if favs_count is None:
    favs_count = Favourite.objects.filter(user=user).count()
    cache.set(cache_key,favs_count,CACHE_EXPIRES)
  
  user_age = user_profile.get_age()

  location = user_profile.location_city 
  if request.user.is_authenticated():
      hasfollowers = has_followers(request.user)
      fe = Fireeagle.objects.filter(user=user,integrated=1)
      if fe:
          location = fe[0].location
  else:
      hasfollowers = None
  #connection.close()
  dict = {'user': user,'user_profile': user_profile,'displayname': get_display_name(user), 'location':location,
          'users_followers': users_followers,'users_followees': users_followees,'followees_count':followees_count, 'followers_count':followers_count,'is_receiver_following':is_receiver_following,
           'is_following':is_following,'is_following_on_im':is_following_on_im,'are_friends':are_friends,'users_friends':users_friends,'user_age':user_age,'has_followers':hasfollowers,
          'logged_in_user_profile':logged_in_user_profile,'profile_for_display':profile_for_display,'favs_count':favs_count,'friends_count':friends_count,} 
  return dict

def everyones_kwips(request,filter):
    page = int(request.GET.get('page',0)) 
    paginate_by = int(request.GET.get('count',20))
    quips_for ='everyone'
    link = '/everyone/'
    max_page=50
    dict = {'location' : 'Hello' }
    if request.user.is_authenticated():
      user_login=request.user.username
    else:
      user_login = 'kwippy'
    filtercount=1
    if filter=="":
        quips = Quip.objects.filter(is_filtered=1).order_by("-id")[(page*paginate_by):((page+1)*paginate_by)]
    elif filter=="active/" or filter=="active":
        quips = Quip.objects.filter(is_filtered=1).order_by("-last_comment_at")[(page*paginate_by):((page+1)*paginate_by)]
        filtercount=2
    #elif (filter=="geo/" or filter=="geo") and request.user.is_authenticated():
    #    feobj = get_object_or_404(Fireeagle, user=request.user)
    #    quips = Quip.objects.everyone_geo(feobj.location,page,paginate_by)
    #    total = quips.count
    #    max_page = total/paginate_by
    #    if total%paginate_by == 0:
    #        max_page= max_page - 1
    #    filtercount=3 
    else:
        raise Http404
    random_users_list = random_users(9)
    # random_users_list = []
    random_users_set = User.objects.filter(id__in=random_users_list)
    active_users_set = active_users(9)
    featured_users_set = Featured_User.objects.all().order_by('-id')[:3]
    rss_users_set = rss_users()
    #active_users_set = []
    #paginator = ObjectPaginator(quips, paginate_by)
    #quips = paginator.get_page(page)
    #feagle=firee(request.user)
    featured_quips = Featured_Kwip.objects.all().order_by('-created_at')[:1]
    #if feagle:
    #    feobj = get_object_or_404(Fireeagle, user=request.user)
    #    dict = { 'location' : feobj.location }
    return render_to_response('mypage.html', {'dict':dict,'is_paginated': True, 'results_per_page': paginate_by,
                              'has_next': page<max_page, 'has_previous': page>0,
                              'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': [],
                              'hits' : 0, 'login': user_login,'quips': quips,'random_users':random_users_set,'rss_users':rss_users_set,
                              'quips_for':quips_for,'filtercount':filtercount,'link':link,'active_users':active_users_set,
                              'featured_users':featured_users_set,'featured_quips':featured_quips,
                              'revision_number': settings.REVISION_NUMBER,}, context_instance=template.RequestContext(request))

def mypage(request,user_login,filter,quips_for):
  if request.user.is_authenticated():
    friendship_requests  = pending_requests(request)
    if friendship_requests:
      friendship_requests = friendship_requests
  else:
    friendship_requests = False
  page = int(request.GET.get('page',0)) 
  paginate_by = int(request.GET.get('count',20))
  login_user = get_object_or_404(User, username=user_login)
  dict = details_for_kwips_page(request,user_login)
  link = ""
  filtercount=1
  #import pdb
  #pdb.set_trace()
  if quips_for=='self':
    if login_user.is_active == 3:
      raise Http404
    link = '/'+user_login+'/kwips/'
    accounts = list(Account.objects.filter(user=dict['user'],status=1))
    if accounts:
      if filter=="":
          quips = Quip.objects.user_kwips(login_user.id,"id",page,paginate_by) #Quip.objects.filter(is_filtered=1).select_related('user','account').order_by("-id")[(page*paginate_by):((page+1)*paginate_by)]
      elif filter=="active/" or filter=="active":
          quips = Quip.objects.user_kwips(login_user.id,"last_comment_at",page,paginate_by) #Quip.objects.filter(is_filtered=1).select_related('user','account').order_by("-last_comment_at")[(page*paginate_by):((page+1)*paginate_by)]
          filtercount=2
      else:
          raise Http404
    else:
      quips = False
  elif quips_for=='all':
    if login_user.is_active == 3:
      raise Http404
    link = '/'+user_login+'/'
    if filter=="":
        quips = Quip.objects.user_network_kwips(login_user.id,"id",page,paginate_by)
    elif filter=="active/" or filter=="active":
        quips = Quip.objects.user_network_kwips(login_user.id,"last_comment_at",page,paginate_by)    
        filtercount=2
    else:
        raise Http404
  total = 400 #quips.count
  max_page = total/paginate_by
  #max_page = 10
  if total%paginate_by == 0:
      max_page= max_page - 1
  feagle=firee(request.user)
  #paginator = ObjectPaginator(quips, paginate_by)
  #quips = paginator.get_page(page)
  if quips:
    return render_to_response('mypage.html', {'is_paginated': True, 'results_per_page': paginate_by,
                              'has_next': page<max_page, 'has_previous': page>0,
                              'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': [],
                              'hits' : 0, 'login': user_login,'quips': quips,
                              'quips_for': quips_for,'dict':dict,'link':link,'filtercount':filtercount,'feagle':feagle,
                              'revision_number': settings.REVISION_NUMBER,'friendship_requests':friendship_requests,
                              'kwip_count':kwip_count(dict['user']),'comment_count':comment_count(dict['user'])}, context_instance=template.RequestContext(request))  
  else:
    return render_to_response('mypage.html', {'login': user_login,'quips': quips,'filtercount':filtercount,'link':link,
                              'quips_for': quips_for,'dict':dict,'friendship_requests':friendship_requests,'feagle':feagle,
                              'revision_number': settings.REVISION_NUMBER,'is_receiver_following':dict['is_receiver_following'],
                              'kwip_count':kwip_count(dict['user']),'comment_count':comment_count(dict['user'])}, context_instance=template.RequestContext(request))  

    
@login_required
def store_kwip(request):
  if request.method == "POST":
    user = get_object_or_404(User, username=request.user)
    if request.META.has_key('HTTP_REFERER'):
      referer = request.META.get('HTTP_REFERER', '')
    else:
      referer = str(user.username)
    account = get_object_or_404(Account, user=user,provider=0,status=1)
    new_kwip = Quip(original=request.POST['kwip_box'].strip(),formated=request.POST['kwip_box'].strip(),account_id=int(account.id),repeat_id=0,user=user,is_filtered=1)
    new_kwip.save()
    up = get_object_or_404(User_Profile,user=request.user)
    up.quip_total = up.quip_total + 1 
    up.save()
    #request.session['flash'] = "Your kwip was saved" 
    #request.flash = "Your kwip was saved" 
  return HttpResponseRedirect(referer)

@login_required
def delete_kwip(request,quip_id):
  quip=get_object_or_404(Quip, id=quip_id)
  if request.user.is_authenticated and quip:    
    if request.user == quip.account.user:
      referer = request.META.get('HTTP_REFERER', '')
      Quip.objects.get(id=quip_id).delete()
      up = get_object_or_404(User_Profile, user=request.user)
      up.quip_total = up.quip_total - 1
      up.save()
      Comment.objects.filter(object_pk=quip_id).delete()
      #request.session['flash'] = "Your kwip was deleted" 
    return HttpResponseRedirect(referer)
  
@login_required
def follow_user(request,followee_username):
  followee_user = get_object_or_404(User, username=followee_username)
  if request.META.has_key('HTTP_REFERER'):
    referer = request.META.get('HTTP_REFERER', '')
  else:
    referer = str(followee_username)
  followee_user = get_object_or_404(User, username=followee_username)
  follower_user = get_object_or_404(User,id=request.user.id)

  if follower_user!=followee_user:
    if request.GET['to_do']=="follow":
      if not Follower.objects.filter(followee=followee_user,follower=follower_user):
          if not follower_user.is_active == 4:
              default_notification_flag = get_object_or_404(User_Profile, user=follower_user).default_notification_on
              if default_notification_flag:
                f=Follower(follower=follower_user,followee=followee_user,im_notification=1)
              else:
                f=Follower(follower=follower_user,followee=followee_user)
              f.save()
              # need to ensure mail type matches the corresponding entry in databases' email table
              params_for_mail = {'#_1':get_display_name(follower_user),'#_2':get_display_name(followee_user), '#_3':follower_user.username}
              send_mail(str(followee_user.email),'kwippy <support@kwippy.com>','follower',params_for_mail)
              send_im(followee_user,'follower',params_for_mail)
	      request.session['flash'] = "You can also set IM notification of kwips by changing the settings."
          else:
              request.session['flash'] = "You are temporarily not allowed to follow someone. Please contact support@kwippy.com"
    else:
      if Follower.objects.filter(followee=followee_user,follower=follower_user):
        #f=Follower.objects.get(followee=followee_user,follower=follower_user)
        f = get_object_or_404(Follower, followee=followee_user, follower=follower_user)
        f.delete()
  cache_key = '%s_follow%dto%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,follower_user.id,followee_user.id,)
  cache.delete(cache_key)
  cache_key = '%s_userfollowerquery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,followee_user.id,)
  cache.delete(cache_key)
  cache_key = '%s_userfollowerqueryfull%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,followee_user.id,)
  cache.delete(cache_key)
  cache_key = '%s_userfolloweequery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,follower_user.id,)
  cache.delete(cache_key)
  cache_key = '%s_followercount%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,followee_user.id,)
  cache.delete(cache_key)
  cache_key = '%s_followeecount%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,follower_user.id,)
  cache.delete(cache_key)
  return HttpResponseRedirect(referer)

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
    request.session['flash'] = "IM notification settings saved" 
  return HttpResponseRedirect(referer)



def follow_user_nomail(follower, followee, im_notification):  
  follower_user = get_object_or_404(User, id=int(follower.id))
  followee_user = get_object_or_404(User, username=str(followee))
  if not Follower.objects.filter(followee=followee_user,follower=follower_user):
    f=Follower(follower=follower_user,followee=followee_user,im_notification=im_notification)
    f.save()  

@login_required
def favourite_kwip(request,quip_id):
  quip= get_object_or_404(Quip, id=int(quip_id))
  if request.user.is_authenticated:
    cache_key = '%s_favcount%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,request.user.id,)
    cache.delete(cache_key)
    cache_key = '%s_fav%d-%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,request.user.id,int(quip_id),)
    cache.delete(cache_key)
    if not Favourite.objects.filter(quip=quip,user=request.user):
      fav = Favourite(user=request.user,quip=quip)
      fav.save()
      if quip.account.user != request.user:
        timestamp = quip.created_at.strftime("%Y/%b/%d/%H%M%S")
        link = str(quip.account.user.username)+'/kwips/'+timestamp.lower()  
        params_for_mail = {'#_1':str(quip.account.user.username),'#_2':str(request.user.username), '#_3':link}
        send_mail(str(quip.account.user.email),'kwippy <support@kwippy.com>','favorite_kwip',params_for_mail)
        send_im(quip.account.user,'favorite_kwip',params_for_mail)
        up = get_object_or_404(User_Profile, user=request.user)
        up.fav_count = up.fav_count+1
        up.save()
      return HttpResponse('Favourited')
    else:
      Favourite.objects.get(quip=quip,user=request.user).delete()
      up = get_object_or_404(User_Profile, user=request.user)
      up.fav_count = up.fav_count-1
      up.save()
      return HttpResponse('UnFavourited')
  return HttpResponse('oops')


#This function will fetch kwips for a particular
#hour, minute or second using custom sqls

def quip_for_a_time(user,filter_by,year,month,day,hour,minute=0,second=0):
  cursor = connection.cursor()
  #getting all accounts
  accounts = Account.objects.filter(user=user,status=1)  
  if accounts:
    accounts_list_in_csv = queryset_to_csv(accounts,'account_forsql')      
    if filter_by=='minute':
      cursor.execute("SELECT id FROM kwippy_quip WHERE account_id in (%s) and year(created_at) = %d and month(created_at) = %d and day(created_at) = %d and hour(created_at) = %d and minute(created_at) = %d" % ( accounts_list_in_csv,int(year),int(month),int(day),int(hour),int(minute)))
    elif filter_by=='second':
        cursor.execute("SELECT id FROM kwippy_quip WHERE account_id in (%s) and year(created_at) = %d and month(created_at) = %d and day(created_at) = %d and hour(created_at) = %d and minute(created_at) = %d and second(created_at)=%d" % ( accounts_list_in_csv,int(year),int(month),int(day),int(hour),int(minute), int(second)))
    else:
      cursor.execute("SELECT id FROM kwippy_quip WHERE account_id in (%s) and year(created_at) = %d and month(created_at) = %d and day(created_at) = %d and hour(created_at) = %d" % ( accounts_list_in_csv,int(year),int(month),int(day),int(hour)))
    quip_ids = [item[0] for item in cursor.fetchall()]
    connection.close()
    return Quip.objects.filter(id__in=quip_ids)


def one_kwip_page(request,user_login,quip_id):
    quip = get_object_or_404(Quip,id=quip_id)
    quips = [quip]
    allow_anon_comm = False
    is_converted = False
    converted_username = False
    if request.user.is_authenticated():
      conv_inv_code = None
      cf = Comment_Follower.objects.filter(user=request.user,quip=quips[0],is_active=0)
      if cf:
          cf = cf[0]
          cf.is_active=1
          cf.save()
    else:
      if request.GET.has_key('inv_code') and is_single:
        conv_inv_code =  request.GET['inv_code']
        #if Anon_Conversation_Invite.objects.filter(quip=quips[0], code=conv_inv_code)
        #invites_for_this_kwip = Anon_Conversation_Invite.objects.filter(quip=quips[0])
        #inv_list = []
        #for item in invites_for_this_kwip:
        #  inv_list.append(item.code)
        #if conv_inv_code in inv_list:
        anon_con_invite = Anon_Conversation_Invite.objects.filter(quip=quips[0], code=conv_inv_code)
        if anon_con_invite:
          allow_anon_comm = True
          user = User.objects.filter(email='anon_'+anon_con_invite[0].receiver)
          if user:
            user = user[0]
            comments = Comment.objects.filter(object_pk=quips[0].id,user=user).order_by('-id')[0]
            if comments:
              is_converted = True
              converted_username = comments.headline
      else:
        conv_inv_code = None
    dict = details_for_kwips_page(request,user_login)
    favorites = Favourite.objects.filter(quip=quip).order_by('-id')
    return render_to_response('mypage.html', {'is_paginated': False, 'results_per_page': 0,
                              'has_next': False, 'has_previous':False,
                              'page': 0, 'next': 0, 'previous': 0, 'pages': 0, 'quips':[quip],'kwip_id':quip_id,'conv_inv_code':conv_inv_code,'is_converted':is_converted,
                              'quips_for': 'self','no_show' : False,'favorites':favorites, 'with_reply_box':False ,'is_single':True,'dict':dict,'login': user_login,'allow_anon_comm':allow_anon_comm,'converted_username':converted_username,
                              'kwip_count':kwip_count(dict['user']),'comment_count':comment_count(dict['user'])},context_instance=template.RequestContext(request))


#This function is called when quips for a date, hour and a minute are needed
def filtered_kwips_page(request,user_login,year,month=0,day=0,hour=0,serial=0,filter_by='day',with_reply_box=False):    
      
  no_show = True
  is_single = False
  paginate_by = 20
  dict = details_for_kwips_page(request,user_login)
  if dict['user'].is_active == 3:
      raise Http404
  month_in_words = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
  
  i=1
  for mon in month_in_words:
    if month==mon:
      month=i
    i=i+1
    
  #getting all accounts for user  
  accounts = Account.objects.filter(user=dict['user'],status=1)
  if accounts:
    kwip_id = None
    accounts_list_in_csv = queryset_to_csv(accounts,'account')
    if filter_by=='year':
      quips =  Quip.objects.filter(account__in=accounts_list_in_csv,created_at__year=int(year)).order_by('-created_at')      
    elif filter_by=='month':
      quips =  Quip.objects.filter(account__in=accounts_list_in_csv,created_at__year=int(year),created_at__month=int(month)).order_by('-created_at')            
    elif filter_by=='date':
      quips =  Quip.objects.filter(account__in=accounts_list_in_csv,created_at__year=int(year),created_at__month=int(month),created_at__day=int(day)).order_by('-created_at')                  
    elif filter_by=='hour':
      quips = quip_for_a_time(dict['user'],filter_by,year,month,day,hour)
    elif filter_by=='minute':
      minute=hour[2]+hour[3]    
      hour = hour[0]+hour[1]    
      quips = quip_for_a_time(dict['user'],filter_by,year,month,day,int(hour),int(minute))
    elif filter_by=='second':
      second=hour[4]+hour[5]
      minute=hour[2]+hour[3]    
      hour = hour[0]+hour[1]      
      quips = quip_for_a_time(dict['user'],filter_by,year,month,day,int(hour),int(minute),int(second))
      if len(quips)==1:
        is_single=True
    elif filter_by=='single':
      second=hour[4]+hour[5]
      minute=hour[2]+hour[3]    
      hour = hour[0]+hour[1]
      quipsnow = quip_for_a_time(dict['user'],filter_by,year,month,day,int(hour),int(minute),int(second))
      is_single=True      
      no_show=True
      for q in quipsnow:
        quips = q.quips_on_same_time_serial(int(serial))
        #break commented by MD
    paginator = Paginator(quips, paginate_by)
    page = int(request.GET.get('page',1)) 
    quips = paginator.page(page)
    quips_list = quips.object_list
    kwip_id = quips_list[0].id

    allow_anon_comm = False
    is_converted = False
    converted_username = False
    if request.user.is_authenticated():
      conv_inv_code = None
      cf = Comment_Follower.objects.filter(user=request.user,quip=quips_list[0],is_active=0)
      if cf:
          cf = cf[0]
          cf.is_active=1
          cf.save()
    else:      
      if request.GET.has_key('inv_code') and is_single:
        conv_inv_code =  request.GET['inv_code']
        #if Anon_Conversation_Invite.objects.filter(quip=quips[0], code=conv_inv_code)
        #invites_for_this_kwip = Anon_Conversation_Invite.objects.filter(quip=quips[0])
        #inv_list = []
        #for item in invites_for_this_kwip:
        #  inv_list.append(item.code)        
        #if conv_inv_code in inv_list:
        anon_con_invite = Anon_Conversation_Invite.objects.filter(quip=quips[0], code=conv_inv_code)
        if anon_con_invite:
          allow_anon_comm = True
          user = User.objects.filter(email='anon_'+anon_con_invite[0].receiver)
          if user:
            user = user[0]            
	    comments = Comment.objects.filter(object_pk=quips[0].id,user=user).order_by('-id')[0]
            if comments:
              is_converted = True
              converted_username = comments.headline
      else:
        conv_inv_code = None
    if is_single:
        favorites = Favourite.objects.filter(quip=quips_list[0]).order_by('-id')
    else:
        favorites = None
    return render_to_response('mypage.html', {'is_paginated': paginator.num_pages > 1, 'results_per_page': paginate_by,
                              'has_next': quips.has_next(), 'has_previous': quips.has_previous(),
                              'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': paginator.num_pages, 'quips':quips_list,'kwip_id':kwip_id,'conv_inv_code':conv_inv_code,'is_converted':is_converted,
                              'quips_for': 'self','no_show' : no_show,'favorites':favorites, 'with_reply_box':with_reply_box,'is_single':is_single,'dict':dict,'login': user_login,'allow_anon_comm':allow_anon_comm,'converted_username':converted_username,
                              'kwip_count':kwip_count(dict['user']),'comment_count':comment_count(dict['user'])},context_instance=template.RequestContext(request))
