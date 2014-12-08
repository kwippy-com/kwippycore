import sha, random,pdb,os,datetime, re,time
from django.conf import settings
from django import template, http
from kwippy.views.comm_queue import send_mail, comm_queue, send_im
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.__init__ import login
from django.contrib.comments.models import Comment
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import InvalidPage
from kwippy.models.notification_setting import NotificationSetting
from kwippy.models.quip import Quip
from kwippy.models.login import Login
from kwippy.models.email import Email
from kwippy.models.email_account import Email_Account
from kwippy.models.email_log import Email_Log
from kwippy.models.follower import Follower
from kwippy.models.friend import Friend
from kwippy.models.fireeagle import Fireeagle
from kwippy.models.favourite import Favourite
from kwippy.models.favourite_comment import Favourite_Comment
from kwippy.models.featured_kwip import Featured_Kwip
from kwippy.models.featured_user import Featured_User
from kwippy.models.account import Account
from kwippy.models.page_setting import PageSetting
from kwippy.models.account_delete import AccountDelete
from kwippy.models.invite import Invite
from kwippy.models.conversation_invite import ConversationInvite
from kwippy.models.anon_conversation_invite import Anon_Conversation_Invite
from kwippy.models.private_message import Private_Message
from kwippy.models.buzz import Buzz
from kwippy.models.theme import Theme
from kwippy.models.user_profile import User_Profile
from kwippy.models.account_delete import AccountDelete
from kwippy.models.beta_invite import Beta_Invite
from kwippyproject.comm_queue_app.models import Commd
from django.contrib.auth.models import *

@login_required
def guppy_status(request):
    import guppy
    heapy = guppy.hpy()
    hp1 = heapy.heap()
    return render_to_response('console/guppy_status.html',dict(hp=hp1[0].byvia))

@login_required
def memcached_status(request):
    import memcache
    # get first memcached URI
    m = re.match(
        "memcached://([.\w]+:\d+)", settings.CACHE_BACKEND
    )
    if not m:
        raise http.Http404
    host = memcache._Host(m.group(1))
    host.connect()
    host.send_cmd("stats")
    class Stats:
        pass
    stats = Stats()
    while 1:
        line = host.readline().split(None, 2)
        if line[0] == "END":
            break
        stat, key, value = line
        try:
            # convert to native type, if possible
            value = int(value)
            if key == "uptime":
                value = datetime.timedelta(seconds=value)
            elif key == "time":
                value = datetime.datetime.fromtimestamp(value)
        except ValueError:
            pass
        setattr(stats, key, value)

    host.close_socket()
    get=stats.cmd_get
    if stats.cmd_get==0:
        get=1;
    return render_to_response(
        'console/memcached_status.html', dict(
            stats=stats,
            hit_rate=100 * stats.get_hits / get,
            time=datetime.datetime.now(), # server time
        ))

@login_required
def roll_pendinginvites(request):
    pending_invites = Beta_Invite.objects.filter(sent_email_status=0)
    for item in pending_invites:
        inv = Invite.objects.filter(invitee_email=str(item.email))
        if not inv:
            invite_hash = generate_invite_code(str(item.email),request.user.email)      
            store_invite_in_db(request, invite_hash, 'console')
            item.sent_email_status=1
            item.save()
    return HttpResponseRedirect('/console/list/beta_emails/')	

@login_required
def popular_kwips(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("select id from kwippy_quip where comment_count < 100 and user_id in (select id from auth_user where is_active=1) order by comment_count desc limit 150;")
        kwip_ids = [item[0] for item in cursor.fetchall()]
        connection.close()
        quips = Quip.objects.filter(id__in=kwip_ids).order_by('-comment_count')
        return render_to_response("console/list_kwips.html",{'quips':quips})

def send_pending_invites(request):
    pending_invites = Beta_Invite.objects.filter(sent_email_status=0)
    rnum = random.randint(1,3)
    user = User.objects.filter(username="dipankar")
    if rnum==2:
        user = User.objects.filter(username="kestrachern")
    elif rnum==3:
        user = User.objects.filter(username="kestrachern")
    request.user = user[0]
    for item in pending_invites:
        inv = Invite.objects.filter(invitee_email=str(item.email))
        if not inv:
            invite_hash = generate_invite_code(str(item.email),request.user.email)
            store_invite_in_db(request, invite_hash, 'console')
            item.sent_email_status=1
            item.save()
    return HttpResponse('')
       
@login_required
def mailfooter(request):
    if request.user.is_superuser:
        if not request.method == "POST":
            footer = get_object_or_404(Email, type='footer')
            return render_to_response("console/mailfooter.html",{'footer':footer})
        else:
            footer = get_object_or_404(Email, type='footer')
            footer.body_text =  request.POST['mail_text']
            footer.body_html = request.POST['mail_html']
            footer.save()
            return render_to_response("console/mailfooter.html",{'footer':footer})
            
@login_required
def mail_all(request):
  if request.method == "POST":    
    mail_subject=request.POST.get('mail_subject')
    mail_body=request.POST.get('mail_body')
    if mail_body and mail_subject:      
      users=User.objects.filter(is_active=1)
      for user in users:
        if user.date_joined!=user.last_login and user.username!='kwippy' and user.username!='admin':
          pdb.set_trace()
          send_mail(str(user.email),'Kwippy <support@kwippy.com>',mail_subject,mail_body)
  else:
    return render_to_response("console/mailer.html")

@login_required
def list_comments(request):
    comments = Comment.objects.all().order_by('-submit_date')[:100]
    return render_to_response("console/list_comments.html",{'comments':comments})

def list_secondaryemails(request):
    email_accs = Email_Account.objects.all().order_by('-updated_at')[:100]
    return render_to_response("console/list_secondaryemails.html",{'email_accs':email_accs})


@login_required
def featured_users(request):
    comments = Comment.objects.all().order_by('-submit_date')[:100]
    featured_users = Featured_User.objects.all()
    return render_to_response("console/featured_users.html",{'featured_users':featured_users})

def feature_new_users(request):
    # criteria for featuring would be on desc order of comments, except team but comment count > 100
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("select count(*) as cnt ,user_id from django_comments where user_id not in (3,4,6,53,1571,465) group by user_id order by cnt desc limit 50;")
    active_users = cursor.fetchall()
    connection.close()
    featured_users = Featured_User.objects.all()
    count = 3
    now = datetime.datetime.now()
    date = now.date()-datetime.timedelta(99)
    for user in active_users:
        #comment count should be greater than 100
        if int(user[0])>15 and count > 0:
            usr = get_object_or_404(User,id=int(user[1]))
            if not Featured_User.objects.filter(user=usr):
                feat_user = Featured_User(user = usr)
                feat_user.save()
                count = count -1
                params_for_mail = {'#_1':usr.username}
                send_mail(str(usr.email),'Kwippy <support@kwippy.com>','featured_user',params_for_mail)
                
    #delete featured users who were featured 99 days back so that they can be featured again.
    old_feat_users = Featured_User.objects.filter(created_at__lte=date)
    old_feat_users.delete()
    featured_users = Featured_User.objects.all()
    return render_to_response("console/featured_users.html",{'featured_users':featured_users})


@login_required
def show_comm_queue(request):
        if request.user.is_superuser:
            commd = Commd.objects.all().order_by('-id')[:30]	
    	    return render_to_response("console/list_comm_queue.html",{'commd':commd})

@login_required
def show_email_log(request):
	log = Email_Log.objects.all().order_by('-created_at')[:20]	
    	return render_to_response("console/email_log.html",{'log':log})

@login_required
def show_anon_conv_invite_log(request):
	log = Anon_Conversation_Invite.objects.all().order_by('-created_at')[:100]
    	return render_to_response("console/anon_conv_invite_log.html",{'log':log})


def featuring(request):
  featured_kwips = Featured_Kwip.objects.all()   
  if request.method == "POST":
      kwip_id = request.POST['kwip_id']
      kwip = get_object_or_404(Quip, id=kwip_id)
      feat_kwip = Featured_Kwip(quip=kwip,user=request.user,email_sent=0)
      feat_kwip.save()
      featured_kwip = Featured_Kwip.objects.all().order_by('-created_at')[:1][0]
      if featured_kwip and not featured_kwip.email_sent:
          user=featured_kwip.quip.account.user
          timestamp = featured_kwip.quip.created_at.strftime("%Y/%b/%d/%H%M%S")
          link = str(user.username)+'/kwips/'+timestamp.lower()
          params_for_mail = {'#_1':user.username,'#_2':link}
          send_mail(str(user.email),'Kwippy <support@kwippy.com>','homepage_feature',params_for_mail)
          featured_kwip.email_sent=1
          featured_kwip.save() 
      return render_to_response("console/mailer.html", {'featured_kwips':featured_kwips} )
  else:
    return render_to_response("console/mailer.html", {'featured_kwips': featured_kwips})

@login_required
def invites_status(request):
  #page = int(request.GET.get('page',0))
  #paginate_by = 15
  invites = Invite.objects.all().order_by('-updated_at')[:100]
  #paginator = ObjectPaginator(invites, paginate_by)    
  #invites = paginator.get_page(page)
    
  #return render_to_response("console/invites_status.html", {'is_paginated': paginator.pages > 1, 'results_per_page': paginate_by,
  #                            'has_next': paginator.has_next_page(page), 'has_previous': paginator.has_previous_page(page),
  #                            'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': paginator.pages,
  #                            'hits' : paginator.hits,'invites':invites})

  return render_to_response("console/invites_status.html", {'invites':invites})


def generate_invite_code(recipient_email,sender_email):
  email_list = []
  email_dict = {}
  if recipient_email:
    recipient_email = recipient_email.split(',')    
    if len(recipient_email) > 1:
      for i in recipient_email:
        email_list.append(i)    
      for i in email_list:
        email_dict[i] = sha.new(i+sender_email+str(random.random())).hexdigest()[:10]
    else:
      email_dict[recipient_email[0]] = sha.new(recipient_email[0]+sender_email+str(random.random())).hexdigest()[:10]
  else:
    email_dict['None'] = sha.new(sender_email+str(random.random())).hexdigest()[:10]
  return email_dict

def generate_otherservice_invites(recipient,sender_email):
    email_dict = {}
    email_dict[recipient] = sha.new(recipient+sender_email+str(random.random())+str(time.time())).hexdigest()[:10]
    return email_dict

def store_invite_in_db(request,email_dict,type):
  for item in email_dict:
      if item=='None':
        inv = Invite(user=request.user,invitee_email=None,invite_type=0,unique_hash=str(email_dict[item]))        
        inv.save()      
      else:
        inv = Invite(user=request.user,invitee_email=str(item),invite_type=0,unique_hash=str(email_dict[item]))
        inv.save()
        if type=='friend':
          send_mail(str(item),'Kwippy <support@kwippy.com>','friend_invite',{'#_1':str(email_dict[item]),'#_2':str(request.user.username)})
        else:
          send_mail(str(item),'Kwippy <support@kwippy.com>','beta_invite',{'#_1':str(email_dict[item])})        
  return

def store_twitter_invite_in_db(request,email_dict):
  for item in email_dict:
        inv = Invite(user=request.user,invitee_email=None,invite_type=2,unique_hash=str(email_dict[item]))        
        inv.save()      
  return


def store_invite_in_db_repeat(request,email_dict,user_list):  
  inv = Invite(user=request.user,invitee_email=str(email_dict.keys()[0]),invite_type=0,unique_hash=str(email_dict.get(email_dict.keys()[0])))               
  inv.save()
  if len(user_list)>0:
    send_mail(str(email_dict.keys()[0]),'Kwippy <support@kwippy.com>','beta_invite',{'#_1':'sexy'})
  else:
    send_mail(str(email_dict.keys()[0]),'Kwippy <support@kwippy.com>','beta_invite',{'#_1':str(email_dict[item])})        
  return


@login_required
def invitation(request):
  if request.user.is_superuser:    
    if request.method == "POST":      
        invite_hash = generate_invite_code( request.POST.get('e-mail'),request.user.email)      
        store_invite_in_db(request, invite_hash, 'console')
        return render_to_response("console/invite.html", {'invite_hash': invite_hash, 'hash_length': len(invite_hash)},  context_instance=template.RequestContext(request))         
    return render_to_response("console/invite.html",context_instance=template.RequestContext(request))     
  else:
    return HttpResponseRedirect('/'+request.user.username+'/')	
    
@login_required
def guestpass(request):
  if request.user.is_superuser:
    if request.method == "POST":
        newpass = request.POST.get('newpass')
        os.system("htpasswd -b "+settings.AUTH_FILE+" guest "+newpass)
  return render_to_response("console/guestpass.html")  

@login_required
def main_view(request):
  if request.user.is_superuser:
    kwippy = User.objects.get(username='kwippy')
    founders = User.objects.filter(id__in=[3,4,6,53])
    rss_users = User.objects.filter(id__in=[7377,7382,7400])
    active_users = User.objects.filter(is_active=1).count()
    inactive_users = User.objects.filter(is_active=0).count()
    active_accounts = Account.objects.filter(status=1).count()
    active_hellotxt_accounts = Account.objects.filter(status=1, provider=13).count()
    active_pingfm_accounts = Account.objects.filter(status=1, provider=12).count()
    active_gtalk_accounts = Account.objects.filter(status=1, provider=2).count()
    active_yahoo_accounts = Account.objects.filter(status=1, provider=7).count()
    active_fb_accounts = Account.objects.filter(status=1, provider=9).count()
    active_web_accounts = Account.objects.filter(status=1, provider=0).count()
    total_kwips = Quip.objects.all().count()
    total_comments = Comment.objects.all().exclude(user__in=founders).count()
    total_private_messages = Private_Message.objects.all().count()
    total_buzzs = Buzz.objects.all().count()    
    total_follows = Follower.objects.exclude(followee=kwippy).count()
    total_im_follows = Follower.objects.filter(im_notification=1).exclude(followee=kwippy).exclude(follower__in=founders,followee__in=founders).count()
    total_friends = Friend.objects.filter(status=1).count()
    total_favorites = Favourite.objects.all().count()
    total_comment_favorites = Favourite_Comment.objects.all().count()
    total_invites = Invite.objects.all().exclude(user__in=founders).count()
    total_conversation_invites =  ConversationInvite.objects.all().exclude(sender__in=founders).count()
    total_acc_deletes = AccountDelete.objects.all().count()
    themes = Theme.objects.all()
    total_theme_users = User_Profile.objects.filter(theme__in=themes).count()
    total_fireeagle_accounts = Fireeagle.objects.all().exclude(user__in=founders).count()
    total_nonusers_invites = Anon_Conversation_Invite.objects.all().exclude(sender__in=founders).count()
    total_secondaryemails = Email_Account.objects.all().count()
    rss_followers = Follower.objects.filter(followee__in=rss_users).count()
    return render_to_response("console/main.html", {'active_users': active_users,'inactive_users':inactive_users, 'active_accounts': active_accounts, 'active_gtalk_accounts':active_gtalk_accounts,'active_fb_accounts':active_fb_accounts,
                                                    'active_yahoo_accounts':active_yahoo_accounts, 'active_web_accounts': active_web_accounts,'active_pingfm_accounts':active_pingfm_accounts,
                                                    'total_comments': total_comments, 'total_follows': total_follows, 'total_buzzs':total_buzzs,'active_hellotxt_accounts':active_hellotxt_accounts,'total_im_follows':total_im_follows,'total_nonusers_invites':total_nonusers_invites,
                                                    'total_private_messages': total_private_messages, 'total_kwips': total_kwips, 'total_comment_favorites':total_comment_favorites,'total_favorites': total_favorites,'total_acc_deletes':total_acc_deletes,'total_theme_users':total_theme_users,'total_fireeagle_accounts':total_fireeagle_accounts, 'total_secondaryemails':total_secondaryemails,                                        'rss_followers':rss_followers,           'total_invites': total_invites,'total_friends':total_friends,'total_conversation_invites':total_conversation_invites})
  else:
    return HttpResponseRedirect('/'+request.user.username+'/')	

@login_required
def toppers(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("select count(*),user_id from django_comments where user_id not in (3,4,6,53) group by user_id order by count(*) desc limit 10;")
        comment_toppers = cursor.fetchall()
        cursor.execute("select count(*),followee_id from kwippy_follower where followee_id not in (3,4,6,53) group by followee_id order by count(*) desc limit 10;")
        follower_toppers = cursor.fetchall()
        cursor.execute("select count(*),follower_id from kwippy_follower where follower_id not in (3,4,6,53) group by follower_id order by count(*) desc limit 10;")
        followee_toppers = cursor.fetchall()
        cursor.execute("select count(*),user_id from kwippy_favourite where user_id not in (3,4,6,53) group by user_id order by count(*) desc limit 10;")
        favorite_toppers =  cursor.fetchall()
        connection.close()
        return render_to_response("console/toppers.html", {'comment_toppers': comment_toppers,'follower_toppers':follower_toppers, 'followee_toppers':followee_toppers, 'favorite_toppers':favorite_toppers})
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')
    
@login_required
def topper_kwips(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        most_commented_quips = Quip.objects.filter(comment_count__gt=0).order_by('-comment_count')[:15]
        cursor.execute("select count(*) as cnt, quip_id from kwippy_favourite group by quip_id order by cnt desc limit 15;")
        most_favorited_quips =  cursor.fetchall()
        connection.close()
        return render_to_response("console/topper_kwips.html", {'most_commented_quips':most_commented_quips,'most_favorited_quips':most_favorited_quips})
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')
    

@login_required
def day_wise_acivity(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("select count(*) as cnt ,date(date_joined) as dt from auth_user where is_active=1  group by date(date_joined) order by date(date_joined) desc limit 14;")
        daily_signups = cursor.fetchall()
        connection.close()
        return render_to_response("console/guestpass.html", {'daily_signups': daily_signups,})
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')	        

@login_required
def day_wise_logins(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("select count(*) from auth_user where datediff(date(now()),date(last_login)) > 7;")
        inactive_users_week = cursor.fetchall()[0][0]
        cursor.execute("select count(*) from auth_user where datediff(date(now()),date(last_login)) > 14;")
        inactive_users_2week = cursor.fetchall()[0][0]
        cursor.execute("select count(*) from auth_user where datediff(date(now()),date(last_login)) > 21;")
        inactive_users_3week = cursor.fetchall()[0][0]
        cursor.execute("select count(*) from auth_user where datediff(date(now()),date(last_login)) > 28;")
        inactive_users_4week = cursor.fetchall()[0][0]
        cursor.execute("select count(*) from auth_user where datediff(date(now()),date(last_login)) > 56;")
        inactive_users_8week = cursor.fetchall()[0][0]
        cursor.execute("select count(*) from auth_user where datediff(date(now()),date(last_login)) > 84;")
        inactive_users_12week = cursor.fetchall()[0][0]
        cursor.execute("select count(*) from auth_user where last_login=date_joined and is_active=1;")
        one_time_loggers = cursor.fetchall()[0][0]
        cursor.execute("select count(*) from auth_user where date(last_login)=date(date_joined) and is_active=1;")
        one_day_loggers = cursor.fetchall()[0][0]
        connection.close()
        return render_to_response("console/daily_logins.html", {'one_time_loggers':one_time_loggers,'one_day_loggers':one_day_loggers,'inactive_users_week':inactive_users_week,'inactive_users_2week':
                                                                inactive_users_2week,'inactive_users_3week':inactive_users_3week, 'inactive_users_4week':inactive_users_4week,
                                                                'inactive_users_8week':inactive_users_8week,'inactive_users_12week':inactive_users_12week})
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')	        

#@login_required
#def account_recover(request):
#    if request.user.is_superuser:
#        user = get_object_or_404(User, username = )
#        user.is_active = 1

@login_required
def unique_weekly_commenters(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("select count(distinct(user_id)) from django_comments where  datediff(date(now()),date(submit_date)) <= 7;")
        last_week_commenters = cursor.fetchall()[0][0]
        cursor.execute("select count(distinct(user_id)) from django_comments where  datediff(date(now()),date(submit_date)) <= 14 and datediff(date(now()),date(submit_date)) > 7;")
        last_2week_commenters = cursor.fetchall()[0][0]
        cursor.execute("select count(distinct(user_id)) from django_comments where  datediff(date(now()),date(submit_date)) <= 21 and datediff(date(now()),date(submit_date)) > 14;")
        last_3week_commenters = cursor.fetchall()[0][0]
        cursor.execute("select count(distinct(user_id)) from django_comments where  datediff(date(now()),date(submit_date)) <= 28 and datediff(date(now()),date(submit_date)) > 21;")
        last_4week_commenters = cursor.fetchall()[0][0]
        cursor.execute("select count(distinct(user_id)) from django_comments where  datediff(date(now()),date(submit_date)) <= 35 and datediff(date(now()),date(submit_date)) > 28;")
        last_5week_commenters = cursor.fetchall()[0][0]
        cursor.execute("select count(distinct(user_id)) from django_comments where  datediff(date(now()),date(submit_date)) <= 42 and datediff(date(now()),date(submit_date)) > 35;")
        last_6week_commenters = cursor.fetchall()[0][0]
        connection.close()
        return render_to_response("console/weekly_commenters.html", {'last_week_commenters':last_week_commenters,'last_2week_commenters':last_2week_commenters,'last_3week_commenters':last_3week_commenters,'last_4week_commenters':last_4week_commenters,'last_5week_commenters':last_5week_commenters,'last_6week_commenters':last_6week_commenters},context_instance=template.RequestContext(request))
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')


@login_required
def averages(request):
    if request.user.is_superuser:
        kwippy = User.objects.get(username='kwippy')
        founders = User.objects.filter(id__in=[3,4,6,53])
        total_users = User.objects.filter(is_active=1).count()
        total_kwips = Quip.objects.all().count()
        total_ims = Account.objects.filter(status=1, provider__in=[2,7]).exclude(user__in=founders).count()
        total_comments = Comment.objects.all().exclude(user__in=founders).count()
        total_private_messages = Private_Message.objects.all().exclude(sender__in=founders).count()
        total_buzzs = Buzz.objects.all().exclude(sender__in=founders).count()
        total_follows = Follower.objects.exclude(followee=kwippy).exclude(follower__in=founders,followee__in=founders).count()
        total_friends = Friend.objects.filter(status=1).count()
        total_favorites = Favourite.objects.all().exclude(user__in=founders).count()
        total_invites = Invite.objects.all().exclude(user__in=founders).count()
        total_conversation_invites =  ConversationInvite.objects.all().exclude(sender__in=founders).count()
        avg_kwips = total_kwips/total_users
        avg_ims = float(total_ims)/total_users
        avg_comments = float(total_comments)/total_users
        avg_pms = float(total_private_messages)/total_users
        avg_buzzes = float(total_buzzs)/total_users
        avg_follows = float(total_follows)/total_users
        avg_friendships = float(total_friends)/total_users
        avg_favorites = float(total_favorites)/total_users
        avg_invites = float(total_invites)/total_users
        avg_conv_invites = float(total_conversation_invites)/total_users
        
        return render_to_response("console/averages.html", {'avg_kwips': avg_kwips,'avg_ims':avg_ims,
                                                            'avg_comments':avg_comments,'avg_pms':avg_pms,'avg_buzzes':avg_buzzes,
                                                            'avg_follows':avg_follows,'avg_friendships':avg_friendships,'avg_favorites':avg_favorites,
                                                            'avg_invites':avg_invites,'avg_conv_invites':avg_conv_invites,})
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')


@login_required
def day_wise_comments(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("select count(*) as cnt ,date(submit_date) as dt from django_comments where user_id not in(3,4,6,53)  group by date(submit_date) order by date(submit_date) desc limit 60;")
        daily_comments = cursor.fetchall()
        cursor.execute("select count(*) from auth_user where id not in (select distinct(user_id) from django_comments);")
        zero_comment_users = cursor.fetchall()[0][0]
        cursor.execute("select sum(comment_count) from kwippy_quip where type <>1 and user_id not in (select distinct(user_id) from django_comments);")
        total_comments_for_zero_comment_users = cursor.fetchall()[0][0]
        cursor.execute("select count(*) from kwippy_quip where comment_count>0 and type <>1 and user_id not in (select distinct(user_id) from django_comments);")
        no_of_kwips_commented = cursor.fetchall()[0][0]
        cursor.execute("select count(*) from django_comments where object_pk in (select quip_id from kwippy_featured_kwip);")
        comments_on_featured = cursor.fetchall()[0][0]
        featured_kwip_count = Featured_Kwip.objects.all().count()
        favorite_kwip_count = Favourite.objects.all().count()
        cursor.execute("select count(*) from django_comments where object_pk in (select distinct(quip_id) from kwippy_favourite);")
        comments_on_favorited = cursor.fetchall()[0][0]
        connection.close()
        fav_comm_ratio = float(comments_on_favorited)/favorite_kwip_count
        return render_to_response("console/daily_comments.html", {'fav_comm_ratio':fav_comm_ratio,'daily_comments': daily_comments,'zero_comment_users':zero_comment_users,'comments_on_featured':comments_on_featured,'featured_kwip_count':featured_kwip_count,'comments_on_favorited':comments_on_favorited,'favorite_kwip_count':favorite_kwip_count,'total_comments_for_zero_comment_users':total_comments_for_zero_comment_users,'no_of_kwips_commented':no_of_kwips_commented})
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')

@login_required
def day_wise_pms(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("select count(*) as cnt ,date(created_at) as dt from kwippy_private_message group by date(created_at) order by date(created_at) desc limit 14;")
        daily_pms = cursor.fetchall()
        connection.close()
        return render_to_response("console/daily_pms.html", {'daily_pms': daily_pms,})
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')

@login_required
def day_wise_favorites(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("select count(*) as cnt ,date(created_at) as dt from kwippy_favourite where user_id not in (3,4,6,53) group by date(created_at) order by date(created_at) desc limit 14;")
        daily_favorites = cursor.fetchall()
        connection.close()
        return render_to_response("console/daily_favorites.html", {'daily_favorites': daily_favorites,})
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')


@login_required
def day_wise_commenters(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("select count(distinct(user_id)) as cnt ,date(submit_date) as dt from django_comments where user_id not in(3,4,6,53)  group by date(submit_date) order by date(submit_date) desc limit 60;")
        daily_commenters = cursor.fetchall()
        connection.close()
        return render_to_response("console/daily_commenters.html", {'daily_commenters': daily_commenters,})
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')
    
@login_required
def day_wise_commentedons(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("select count(distinct(object_pk)) as cnt ,date(submit_date) as dt from django_comments where user_id not in(53)  group by date(submit_date) order by date(submit_date) desc limit 14;")
        day_wise_commentedons = cursor.fetchall()
        connection.close()
        return render_to_response("console/daily_commentedons.html", {'day_wise_commentedons': day_wise_commentedons,})
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')
    
@login_required
def day_wise_betainvites(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("select count(*) as cnt ,date(created_at) as dt from kwippy_beta_invite group by date(created_at) order by date(created_at) desc limit 14;")
        daily_betainvites = cursor.fetchall()
        connection.close()
        return render_to_response("console/daily_betainvites.html", {'daily_betainvites': daily_betainvites,})
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')


@login_required
def day_wise_convinvites(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("select count(*) as cnt ,date(created_at) as dt from kwippy_conversationinvite where sender_id not in (3,4,6) group by date(created_at) order by date(created_at) desc limit 14;")
        daily_convinvites = cursor.fetchall()
        #cursor.execute("select count(*) as cnt ,date(created_at) as dt from kwippy_conversationinvite where sender_id not in (3,4,6) group by date(created_at),quip_id order by date(created_at) desc limit 14;")
        cursor.execute(" select count(distinct(quip_id)),date(created_at) from kwippy_conversationinvite group by date(created_at) order by date(created_at) desc limit 14;")
        daily_convinvites_onkwips = cursor.fetchall()
        cursor.execute("select count(*) from auth_user where id in (select user_id from django_comments);")
        total_anon_users = cursor.fetchall()[0][0]
        cursor.execute("select count(*) from django_comments")
        total_anon_comments = cursor.fetchall()[0][0]
        connection.close()
        return render_to_response("console/daily_invite_to_conv.html", {'daily_convinvites': daily_convinvites,'total_anon_users':total_anon_users,'total_anon_comments':total_anon_comments,'daily_convinvites_onkwips':daily_convinvites_onkwips})
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')

@login_required
def daily_follows(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("select count(*) as cnt ,date(created_at) as dt from kwippy_follower group by date(created_at) order by date(created_at) desc limit 14;")
        daily_follows = cursor.fetchall()
        connection.close()
        return render_to_response("console/daily_follows.html", {'daily_follows': daily_follows,})
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')


@login_required
def twittervirality(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        founders = User.objects.filter(id__in=[3,4,6,53])        
        total_invites = Invite.objects.filter(invite_type=2).exclude(user__in=founders).count()
        total_invites_converted = Invite.objects.filter(invite_type=2,status=2).exclude(user__in=founders).count()
        cursor.execute("select count(*),user_id from kwippy_invite where invite_type=2 and user_id not in (3,4,6,53) group by user_id order by count(*) desc;")
        invite_stats = cursor.fetchall()
        cursor.execute("select count(distinct(user_id)) from kwippy_invite where invite_type=2 and user_id not in (3,4,6,53);")
        total_invitees = cursor.fetchone()[0]
        connection.close()
        return render_to_response("console/twittervirality.html", {'total_invites': total_invites,'invite_stats':invite_stats,
                                  'total_invites_converted':total_invites_converted,'total_invitees':total_invitees})
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')	
    
@login_required
def dailytwittervirality(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        founders = User.objects.filter(id__in=[3,4,6,53])        
        #total_invites = Invite.objects.filter(invite_type=2).exclude(user__in=founders).count()
        #total_invites_converted = Invite.objects.filter(invite_type=2,status=2).exclude(user__in=founders).count()
        cursor.execute("select count(distinct(user_id)),date(created_at) from kwippy_invite where invite_type=2 and user_id not in (3,4,6,53) group by date(created_at) order by date(created_at) desc;")
        invite_sent = cursor.fetchall()
        connection.close()
        return render_to_response("console/dailytwittervirality.html", {'invite_sent':invite_sent,})
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')    

@login_required
def notifications(request):
    if request.user.is_superuser:
        #from django.db import connection
        #cursor = connection.cursor()
        not_settings_all_email_on = NotificationSetting.objects.filter(email='1,1,1,1,0,1,1,1').count()
        not_settings_all_im_on = NotificationSetting.objects.filter(im='1,1,1,1,1,1,1,1').count()
        not_settings_all_email_off = NotificationSetting.objects.filter(email='0,0,0,0,0,0,0,0').count()
        not_settings_all_im_off = NotificationSetting.objects.filter(im='0,0,0,0,0,0,0,0').count()
        both_not_off =  NotificationSetting.objects.filter(im='0,0,0,0,0,0,0,0',email='0,0,0,0,0,0,0,0').count()
        return render_to_response("console/notifications.html", {'not_settings_all_email_on': not_settings_all_email_on,
        'not_settings_all_im_on':not_settings_all_im_on,'not_settings_all_email_off':not_settings_all_email_off,
        'not_settings_all_im_off':not_settings_all_im_off,'both_not_off':both_not_off,
        })
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')

@login_required
def agewise(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        born_after_95 = User_Profile.objects.filter(birth_year__gt=1995).count()
        born_between_85_95 = User_Profile.objects.filter(birth_year__gt=1985,birth_year__lte=1995).count()
        born_between_75_85 = User_Profile.objects.filter(birth_year__gt=1975,birth_year__lte=1985).count()
        born_between_65_75 = User_Profile.objects.filter(birth_year__gt=1965,birth_year__lte=1975).count()
        born_between_55_65 = User_Profile.objects.filter(birth_year__gt=1955,birth_year__lte=1965).count()
        born_between_45_55 = User_Profile.objects.filter(birth_year__gt=1945,birth_year__lte=1955).count()
        born_between_35_45 = User_Profile.objects.filter(birth_year__gt=1935,birth_year__lte=1945).count()
        born_between_25_35 = User_Profile.objects.filter(birth_year__gt=1925,birth_year__lte=1935).count()
        #born_between_ = User_Profile.objects.filter(birth_year__gt=1960,birth_year__lte=1965).count()
        #born_before_60 = User_Profile.objects.filter(birth_year__lte=1960).count()
        cursor.execute("select count(*) as cnt,birth_year from kwippy_user_profile where birth_year is not null and birth_year>0 group by birth_year order by birth_year asc;");
        age_dist =  cursor.fetchall()
        connection.close()
        total = User_Profile.objects.filter(birth_year__isnull=False).exclude(birth_year=0).count()
        return render_to_response("console/agewise.html", {'born_after_95': born_after_95,
        'born_between_85_95':born_between_85_95,'born_between_75_85':born_between_75_85,'born_between_65_75':
        born_between_65_75,'born_between_55_65':born_between_55_65,'born_between_45_55':born_between_45_55,
        'born_between_35_45':born_between_35_45,'total':total,'born_between_25_35':born_between_25_35,'age_dist':age_dist})
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')

@login_required
def virality(request):
    if request.user.is_superuser:
        from django.db import connection
        cursor = connection.cursor()
        founders = User.objects.filter(id__in=[3,4,6])
        total_invites = Invite.objects.all().exclude(user__in=founders).count()
        total_invites_converted = Invite.objects.filter(status=2).exclude(user__in=founders).count() 
        cursor.execute("select count(distinct(user_id)) from kwippy_invite where user_id not in (3,4,6);")
        total_invitees = cursor.fetchone()[0]
        cursor.execute(" select count(*) as cnt ,date(created_at) as dt from kwippy_invite where user_id not in(3,4,6) group by date(created_at) order by date(created_at) desc limit 14;")
        daily_virality = cursor.fetchall()
        connection.close()
        return render_to_response("console/virality.html", {'total_invites': total_invites,'daily_virality':daily_virality,
                                  'total_invites_converted':total_invites_converted,'total_invitees':total_invitees})
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')	

    
@login_required
def listemail(request):
  if request.user.is_superuser:    
    all_entries = Beta_Invite.objects.all().order_by('-created_at')[:100]
    return render_to_response("console/beta_email.html", {'emails':all_entries})
  else:
    return HttpResponseRedirect('/'+request.user.username+'/')	

@login_required
def last_logged_in_users(request,count=10):
  if request.user.is_superuser:
      founders = User.objects.filter(id__in=[3,4,6,53])
      users = User.objects.order_by('-last_login')[:count]
      new_users = User.objects.order_by('-date_joined')[:count]
      comments = Comment.objects.exclude(user__in=founders).order_by('-submit_date')[:count]
      kwippy = User.objects.get(username='kwippy')
      new_followers = Follower.objects.exclude(followee=kwippy).order_by('-created_at')[:count]
      new_friends = Friend.objects.all().order_by('-created_at')[:count]
      new_favorites = Favourite.objects.all().order_by('-created_at')[:count]
      new_favorites_comments = Favourite_Comment.objects.all().order_by('-created_at')[:count]
      new_messages = Private_Message.objects.all().order_by('-created_at')[:count]
      new_buzzes = Buzz.objects.all().order_by('-created_at')[:count]
      new_conv_invites = ConversationInvite.objects.all().order_by('-created_at')[:count]
      new_acc_deletes = AccountDelete.objects.all().order_by('-created_at')[:count]
      new_fb_accounts = Account.objects.filter(status = 1, provider=9).order_by('-created_at')[:count]
      return render_to_response("console/last_loggedin_users.html", {'new_users': new_users, 'users': users, 'comments': comments,'new_acc_deletes':new_acc_deletes,
                                                                    'new_followers': new_followers,'new_friends':new_friends, 'new_favorites':new_favorites,
                                                                    'new_favorites_comments':new_favorites_comments,
                                                                     'new_messages':new_messages,'new_buzzes':new_buzzes,'new_conv_invites':new_conv_invites,
                                                                     'new_fb_accounts':new_fb_accounts})
  else:
    return HttpResponseRedirect('/'+request.user.username+'/')	

@login_required
def birthdays(request):
   if request.user.is_superuser:
       from django.db import connection
       cursor = connection.cursor()
       birth_day_users = User_Profile.objects.filter(birth_day__isnull=False,birth_month__isnull=False).exclude(birth_day=0,birth_month=0).count()
       cursor.execute("select u.username as name ,up.birth_day as birth_date from auth_user u, kwippy_user_profile up where up.user_id= u.id and up.birth_month=month(now()) and up.birth_day>=day(now()) order by up.birth_day;")
       birthdays = cursor.fetchall()
       connection.close()
       return render_to_response("console/birthdays.html",{'birthdays':birthdays,'birth_day_users':birth_day_users})
   else:
       return HttpResponseRedirect('/'+request.user.username+'/')


#@login_required
#def engagement(request):
#    if request.user.is_superuser:
 #       daily_web_kwips = Quip.objects.filter(
  #      return render_to_response("console/notifications.html", {'not_settings_all_email_on': not_settings_all_email_on,
   #     'not_settings_all_im_on':not_settings_all_im_on,'not_settings_all_email_off':not_settings_all_email_off,
    #    'not_settings_all_im_off':not_settings_all_im_off,'both_not_off':both_not_off,
     #   })
    #else:
     #   return HttpResponseRedirect('/'+request.user.username+'/')
   
def send_bday_email(request):
    if request.user.is_superuser:
        if request.method == "POST":
            now = datetime.datetime.now()
            user_profiles = User_Profile.objects.filter(birth_day = now.day, birth_month = now.month)
            if user_profiles:
                email = get_object_or_404(Email, type='birthday')
                for up in user_profiles:
                    if up.user.is_active == 1:
                        params_for_mail = {'#_1':up.user.username}
                        # to ensure that no user gets bday emails twice, this solution will work just for just an year.
                        if not Email_Log.objects.filter(receiver=up.user):
                            send_mail(str(up.user.email),'kwippy <support@kwippy.com>','birthday',params_for_mail)
                            email_log = Email_Log(type=1,receiver=up.user)
                            email_log.save()
                            #request.flash = "Today's birthday mails were sent"
                            #return render_to_response('console/birthdays.html', context_instance=template.RequestContext(request))  
                        #send_im(up.user,'birthday',params_for_mail)                    
            return HttpResponseRedirect('/console/birthdays/')
        else:
            return HttpResponseRedirect('/console/birthdays/')
   
#@login_required
#def two_week_old_users(request):
#    if request.user.is_superuser:
#        from django.db import connection
#        cursor = connection.cursor()
#        cursor.execute("select id,date_joined from auth_user where datediff(date(now()),date(date_joined))<=14;")
#        users_signedup = cursor.fetchall().count()
#        select count(*) from kwippy_quip where user_id in (select id from auth_user where datediff(date(now()),date(date_joined))<=14);
#        select count(*) from kwippy_account where provider<> 0 and user_id in (select id from auth_user where datediff(date(now()),date(date_joined))<=14);
#        select count(*) from kwippy_user_profile where quip_total=1;

@login_required
def createRssUser(request):
    if request.user.is_superuser:
        if request.method == "POST":
            username = request.POST.get("username",False)
            url = request.POST.get("url",False)
            if username and url:
                cuser = User(username=username,email=username+"@kwippy.com")
                cuser.set_password("RandomRSSPassword")
                cuser.save()
                cpagesetting = PageSetting(user=cuser,show_repeat=True)
                cpagesetting.save()
                random_hash = sha.new(str(cuser.email)+str(random.random())).hexdigest()[:10]
                cprofile = User_Profile(user=cuser,display_name=username,hash=random_hash)
                cprofile.save()
                caccount = Account(user=cuser,provider_login=url,provider=14,status=1)
                caccount.save()
            return render_to_response("console/rss_user.html")
        else:
            return render_to_response("console/rss_user.html")
    else:
       return HttpResponseRedirect('/'+request.user.username+'/')

@login_required
def acc_delete(request):
  if request.user.is_superuser:
    if request.method == "POST": 
        # set is_active = 3, give 404 for kwips pages,comments page, favs page, delete followers,followees
        user_login = request.POST['username']
        user = get_object_or_404(User, username=user_login)
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("update auth_user set is_active=3 where id= %d" %int(user.id))
        connection.close()
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
            
    else:
        return render_to_response("console/acc_delete.html")
    return HttpResponseRedirect('/') 


