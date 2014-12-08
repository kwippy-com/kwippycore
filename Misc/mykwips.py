from django.contrib.auth.models import *
from django import oldforms, template, http
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import ObjectPaginator, InvalidPage
from django.views.generic.simple import direct_to_template, redirect_to
from django.conf import settings
from django.template import RequestContext
from django.db import connection
from django.core.cache import *
from kwippy.models.quip import Quip
from kwippy.models.invite import Invite
from kwippy.models.account import Account
from django.contrib.comments.models import Comment
from kwippy.models.follower import Follower
from kwippy.models.favourite import Favourite
from kwippy.models.page_setting import PageSetting
from kwippy.models.user_profile import User_Profile
from kwippy.views.views import queryset_to_csv
from kwippy.views.main import get_display_name, comment_count, kwip_count
from kwippy.views.comm_queue import send_mail,send_im
import pdb


CACHE_EXPIRES = 5 * 60

def isfollowing(follower,followee):
  f = Follower.objects.filter(follower=follower,followee=followee)
  if f:
    return True
  else:
    return False

def details_for_kwips_page(request,user_login):
  from django.db import connection
  cursor = connection.cursor()
  user = get_object_or_404(User, username=user_login)
  if request.user.is_authenticated():
    logged_in_user_profile = User_Profile.objects.get(user=request.user.id)
  else:
    logged_in_user_profile = False
  if request.user.is_authenticated():
    is_following = isfollowing(request.user,user)
    if is_following:
      is_following_on_im = get_object_or_404(Follower, follower=request.user,followee=user).im_notification
    else:
      is_following_on_im = False
    is_receiver_following = isfollowing(user,request.user)
  else:
    is_following_on_im = False 
    is_following = False
    is_receiver_following = False
  user_profile = User_Profile.objects.filter(user=user.id)
  if user_profile:
    user_profile = user_profile[0]
    profile_for_display = {'gender':user_profile.get_gender_display(), 'relationship': user_profile.get_relationship_status_display()}
  ## need to add a display limit to this list
  #followees = user.follower.all().order_by('-created_at')
  #followers = user.followee.all().order_by('-created_at')  
  #followees_list_in_csv = queryset_to_csv(followees,'followee')
  #followers_list_in_csv = queryset_to_csv(followers,'follower')
  ##commented to send user objects to mykwips page inplace of user_profile objects as previously
  #users_followers = User.objects.filter(id__in=followers_list_in_csv).order_by('-last_login').exclude(id=user.id)
  #followers_count = len(users_followers)
  #users_followers = users_followers[:24]    
  #users_followees = User.objects.filter(id__in=followees_list_in_csv).order_by('-last_login').exclude(id=user.id)
  #followees_count = len(users_followees)
  #users_followees = users_followees[:9]
  cursor.execute("select auth_user.id from auth_user,kwippy_follower where kwippy_follower.follower_id=auth_user.id and kwippy_follower.followee_id=%s order by auth_user.last_login desc limit 24",(user.id,))
  followers_ids = [item[0] for item in cursor.fetchall()]
  users_followers = User.objects.filter(id__in=followers_ids).order_by('-last_login') 
  cursor.execute("select auth_user.id from auth_user,kwippy_follower where kwippy_follower.followee_id=auth_user.id and kwippy_follower.follower_id=%s order by auth_user.last_login desc limit 9",(user.id,))
  followees_ids = [item[0] for item in cursor.fetchall()]
  users_followees = User.objects.filter(id__in=followees_ids).order_by('-last_login')
  cursor.execute('select count(*) from kwippy_follower where followee_id=%s',(user.id,))
  (followers_count,)=cursor.fetchone()
  cursor.execute('select count(*) from kwippy_follower where follower_id=%s',(user.id,))
  (followees_count,)=cursor.fetchone() 
  favs_count = Favourite.objects.filter(user=user).count()
  dict = {'user': user,'user_profile': user_profile,'displayname': get_display_name(user),
          'users_followers': users_followers,'users_followees': users_followees,'followees_count':followees_count, 'followers_count':followers_count,'is_receiver_following':is_receiver_following,
           'is_following':is_following,'is_following_on_im':is_following_on_im,
          'logged_in_user_profile':logged_in_user_profile,'profile_for_display':profile_for_display,'favs_count':favs_count,} 
  return dict


def everyones_kwips(request):
    from django.db import connection
    cursor = connection.cursor()
    page = int(request.GET.get('page',0)) 
    paginate_by = 10
    quips_for ='everyone'
    if request.user.is_authenticated():
      user_login=request.user.username
    else:
      user_login = 'kwippy'
   # cursor.execute("select kwippy_quip.id from kwippy_quip,kwippy_account where kwippy_account.id=kwippy_quip.account_id and kwippy_quip.repeat_id in (kwippy_quip.id,0) and kwippy_quip.formated not in ('Away','Available','Logged Out') and kwippy_account.user_id>0 order by id desc limit 1000")
    cursor.execute("select id from kwippy_quip where repeat_id in (id,0) and formated not in ('Away','Available','Logged Out')and  account_id in (select id from kwippy_account where status=1 and user_id>0) order by id desc limit 1000") 
    quip_ids = [item[0] for item in cursor.fetchall()]
    quips = Quip.objects.filter(id__in=quip_ids).order_by('-created_at')
    #cursor.execute(
      #"select distinct(account_id) from kwippy_quip order by id desc limit 100")
      ##"select distinct(q.account_id) from kwippy_quip q, kwippy_account a where a.id=q.account_id and a.user_id>1 order by q.created_at desc limit 100")
    #account_ids = [int(item[0]) for item in cursor.fetchall()]
    #quips =  Quip.objects.filter(id=0)    
    #for acc_id in account_ids:
      #cursor.execute("select * from kwippy_quip where account_id = %d order by created_at desc limit 1" % (acc_id))
      #quip_id = [item[0] for item in cursor.fetchall()]
      #kwip = Quip.objects.filter(id=int(quip_id[0]))
      #quips = quips | kwip
    #quips = quips.order_by('-created_at')
    #quips =  Quip.objects.all().exclude(original='I&apos;m not here right now').order_by('-created_at')[:100]
    
    dict = details_for_kwips_page(request,user_login)
    paginator = ObjectPaginator(quips, paginate_by)
    quips = paginator.get_page(page)    
    return render_to_response('mypage.html', {'is_paginated': paginator.pages > 1, 'results_per_page': paginate_by,
                              'has_next': paginator.has_next_page(page), 'has_previous': paginator.has_previous_page(page),
                              'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': paginator.pages,
                              'hits' : paginator.hits, 'login': user_login,'user_profile': dict['user_profile'],'quips': quips,
                              'users_followees': dict['users_followees'], 'users_followers': dict['users_followers'], 'displayname': dict['displayname'],
                              'followees_count':dict['followees_count'], 'followers_count':dict['followers_count'], 'is_receiver_following':dict['is_receiver_following'],
                              'quips_for': quips_for,'is_following': dict['is_following'],'is_following_on_im': dict['is_following_on_im'],
                              'logged_in_user_profile': dict['logged_in_user_profile'], 'profile_for_display': dict['profile_for_display'],'favs_count':dict['favs_count'],
                              'kwip_count':kwip_count(dict['user']),'comment_count':comment_count(dict['user']),                                              
                              'revision_number': settings.REVISION_NUMBER,}, context_instance=template.RequestContext(request))  
  


def mypage(request,user_login,quips_for):
  
  cursor = connection.cursor()

  page = int(request.GET.get('page',0)) 
  if request.GET.get('page') and page==0:
    if quips_for=='all':
      return HttpResponseRedirect('/'+user_login+'/')
    else:
      return HttpResponseRedirect('/'+user_login+'/'+'kwips/')  
  paginate_by = 10
  login_user = get_object_or_404(User, username=user_login)
  #ques = fb_question_for_page(request.user,'mypage')
  dict = details_for_kwips_page(request,user_login)  
  if quips_for=='self':
    accounts = Account.objects.filter(user=dict['user'],status=1)
    if accounts:
      show_repeat = get_object_or_404(PageSetting, user=login_user).show_repeat
      if show_repeat==1:
        #accounts_list_in_csv = queryset_to_csv(accounts,'account')      
        cursor.execute("select kwippy_quip.id from kwippy_quip,kwippy_account where kwippy_account.id=kwippy_quip.account_id and kwippy_account.user_id=%s and kwippy_account.status=1 and kwippy_quip.formated not in ('Away','Available','Logged Out')  order by id desc limit 1000", (login_user.id,))
        quip_ids = [item[0] for item in cursor.fetchall()]
        #quips =  Quip.objects.filter(account__in=accounts_list_in_csv).exclude(original='Away').order_by('-created_at')
	quips = Quip.objects.filter(id__in=quip_ids).order_by('-created_at')
        #quips =  Quip.objects.extra(where=['account_id IN %s','repeat_id=id'],params=[(accounts_list_in_csv)]).order_by('-created_at')
      else:
        #accounts_list_in_csv = queryset_to_csv(accounts,'account_forsql')      
        #cursor.execute("SELECT * FROM kwippy_quip WHERE account_id in (%s) and repeat_id in (id,0) and formated not in ('Away','Idle'  )" % ( accounts_list_in_csv))
        cursor.execute("select kwippy_quip.id from kwippy_quip,kwippy_account where kwippy_account.id=kwippy_quip.account_id and kwippy_account.user_id=%s and kwippy_account.status=1 and kwippy_quip.repeat_id in (kwippy_quip.id,0) and kwippy_quip.formated not in ('Away','Available','Logged Out')  order by id desc limit 1000", (login_user.id,))
        quip_ids = [item[0] for item in cursor.fetchall()]
        quips = Quip.objects.filter(id__in=quip_ids).order_by('-created_at')
  elif quips_for=='all':
    #quips=Quip.objects.filter(id=0)
    #for item in dict['followees']:
      #accounts=Account.objects.filter(user=item.followee)
      #q1=Quip.objects.filter(account__in=accounts, created_at__gt=item.created_at).order_by('-created_at')
      #quips=quips|q1
    ##adding kwips for the logged in user to the queryset
    #accounts=Account.objects.filter(user=dict['user'])
    #quips = quips | Quip.objects.filter(account__in=accounts).order_by('-created_at')    
    #followees_list_in_csv = queryset_to_csv(dict['followees'],'followee')
    #accounts = Account.objects.filter(user__in=followees_list_in_csv,status=1)
    #accounts = accounts | Account.objects.filter(user=dict['user'])
    #accounts_list_in_csv = queryset_to_csv(accounts,'account_forsql')
    #cursor.execute("SELECT * FROM kwippy_quip WHERE account_id in (%s) and repeat_id in (id,0) and formated not in ('Away','Idle')" % ( accounts_list_in_csv))
    #cursor.execute("select kwippy_quip.id from kwippy_quip,kwippy_account where kwippy_account.id=kwippy_quip.account_id and  kwippy_quip.repeat_id in (kwippy_quip.id,0) and kwippy_quip.formated not in ('Away','Available','Logged Out') and kwippy_account.user_id in (select follower_id from kwippy_follower where followee_id=%s) union select kwippy_quip.id from kwippy_quip,kwippy_account where kwippy_account.id=kwippy_quip.account_id and kwippy_account.user_id=%s order by id desc limit 1000", (login_user.id,login_user.id,))
    cursor.execute("select id from kwippy_quip where repeat_id in (id,0) and formated not in ('Away','Available','Logged Out') and  account_id in (select id from kwippy_account where status=1 and user_id in (select followee_id from kwippy_follower where follower_id=%s) union select id from kwippy_account where user_id=%s) order by id desc limit 1000", (login_user.id,login_user.id,)) 

    quip_ids = [item[0] for item in cursor.fetchall()]
    quips = Quip.objects.filter(id__in=quip_ids).order_by('-created_at')
  if quips:
    paginator = ObjectPaginator(quips, paginate_by)
    quips = paginator.get_page(page)
    return render_to_response('mypage.html', {'is_paginated': paginator.pages > 1, 'results_per_page': paginate_by,
                              'has_next': paginator.has_next_page(page), 'has_previous': paginator.has_previous_page(page),
                              'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': paginator.pages,
                              'hits' : paginator.hits, 'login': user_login,'user_profile': dict['user_profile'],'quips': quips,'favs_count':dict['favs_count'],
                              'users_followees': dict['users_followees'], 'users_followers': dict['users_followers'], 'displayname': dict['displayname'],
                              'followees_count':dict['followees_count'], 'followers_count':dict['followers_count'],'is_receiver_following':dict['is_receiver_following'],
                              'quips_for': quips_for,'is_following': dict['is_following'],'is_following_on_im': dict['is_following_on_im'],
                              'logged_in_user_profile': dict['logged_in_user_profile'], 'profile_for_display': dict['profile_for_display'],
                              'revision_number': settings.REVISION_NUMBER,
                              'kwip_count':kwip_count(dict['user']),'comment_count':comment_count(dict['user'])}, context_instance=template.RequestContext(request))  
  else:
    return render_to_response('mypage.html', {'login': user_login,'user_profile': dict['user_profile'],
                              'users_followees': dict['users_followees'], 'users_followers': dict['users_followers'],
                              'followees_count':dict['followees_count'], 'followers_count':dict['followers_count'], 'displayname': dict['displayname'],
                              'quips_for': quips_for,'is_following': dict['is_following'],'is_following_on_im': dict['is_following_on_im'],'favs_count':dict['favs_count'],
                              'logged_in_user_profile': dict['logged_in_user_profile'], 'profile_for_display': dict['profile_for_display'],
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
    new_kwip = Quip(original=request.POST['kwip_box'].strip(),formated=request.POST['kwip_box'].strip(),account_id=int(account.id),repeat_id=0)
    new_kwip.save()
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
      Comment.objects.filter(object_id=quip_id).delete()
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
          f=Follower(follower=follower_user,followee=followee_user)
          f.save()
          # need to ensure mail type matches the corresponding entry in databases' email table
          params_for_mail = {'#_1':get_display_name(follower_user),'#_2':get_display_name(followee_user), '#_3':follower_user.username}
          send_mail(str(followee_user.email),'kwippy <support@kwippy.com>','follower',params_for_mail)
          send_im(followee_user,'follower',params_for_mail)
	  request.session['flash'] = "You can also set IM notification of kwips by changing the settings." 
    else:
      if Follower.objects.filter(followee=followee_user,follower=follower_user):
        #f=Follower.objects.get(followee=followee_user,follower=follower_user)
        f = get_object_or_404(Follower, followee=followee_user, follower=follower_user)         
        f.delete()
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
  quip= get_object_or_404(Quip, id=quip_id)
  if request.user.is_authenticated:
    if not Favourite.objects.filter(quip=quip,user=request.user):
      fav = Favourite(user=request.user,quip=quip)
      fav.save()
      if quip.account.user != request.user:
        timestamp = quip.created_at.strftime("%Y/%b/%d/%H%M%S")
        link = str(quip.account.user.username)+'/kwips/'+timestamp.lower()  
        params_for_mail = {'#_1':str(quip.account.user.username),'#_2':str(request.user.username), '#_3':link}
        send_mail(str(quip.account.user.email),'kwippy <support@kwippy.com>','favorite_kwip',params_for_mail)
        send_im(quip.account.user,'favorite_kwip',params_for_mail)
      return HttpResponse('Favourited')
    else:
      Favourite.objects.get(quip=quip,user=request.user).delete()
      return HttpResponse('UnFavourited')      
  return HttpResponse('oops')


#This function will fetch kwips for a particular
#hour, minute or second using custom sqls

def quip_for_a_time(user,filter_by,year,month,day,hour,minute=0,second=0):
  from django.db import connection
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
    return Quip.objects.filter(id__in=quip_ids)



#This function is called when quips for a date, hour and a minute are needed
def filtered_kwips_page(request,user_login,year,month=0,day=0,hour=0,serial=0,filter_by='day',with_reply_box=False):
  
  is_single = False
  paginate_by = 10
  dict = details_for_kwips_page(request,user_login)     
  month_in_words = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
  
  i=1
  for mon in month_in_words:
    if month==mon:
      month=i
    i=i+1
    
  #getting all accounts for user  
  accounts = Account.objects.filter(user=dict['user'],status=1)
  if accounts:
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
      for q in quipsnow:
        quips = q.quips_on_same_time_serial(int(serial))
        #break commented by MD
    paginator = ObjectPaginator(quips, paginate_by)
    page = int(request.GET.get('page',0)) 
    quips = paginator.get_page(page)
    return render_to_response('mypage.html', {'is_paginated': paginator.pages > 1, 'results_per_page': paginate_by,
                              'has_next': paginator.has_next_page(page), 'has_previous': paginator.has_previous_page(page),
                              'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': paginator.pages, 'is_following': dict['is_following'],'is_following_on_im': dict['is_following_on_im'],
                              'hits' : paginator.hits, 'login': user_login,'user_profile': dict['user_profile'],'quips': quips,'is_receiver_following':dict['is_receiver_following'],
                              'users_followees': dict['users_followees'], 'users_followers': dict['users_followers'], 'profile_for_display': dict['profile_for_display'],
                              'followees_count':dict['followees_count'], 'followers_count':dict['followers_count'],'displayname': dict['displayname'],'favs_count':dict['favs_count'],
                              'quips_for': 'self','with_reply_box':with_reply_box,'is_single':is_single,
                              'kwip_count':kwip_count(dict['user']),'comment_count':comment_count(dict['user'])},context_instance=template.RequestContext(request))



