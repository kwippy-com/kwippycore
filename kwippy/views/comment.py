from django.contrib.comments.models import Comment
from django.contrib.comments.views.comments import post_comment
from signup_app.forms import SignupForm, SignupFormUniqueEmail 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import *
from kwippy.models.quip import Quip
from kwippy.models.user_profile import User_Profile
from kwippy.models.invite import Invite
from kwippy.models.comment_follower import Comment_Follower
from kwippyproject.kwippy.models.anon_comment_follower import Anon_Comment_Follower
from kwippyproject.kwippy.models.page_setting import PageSetting
from kwippyproject.kwippy.models.notification_setting import NotificationSetting
from kwippy.models.anon_conversation_invite import Anon_Conversation_Invite
from kwippy.models.favourite_comment import Favourite_Comment
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from kwippy.views.comm_queue import send_mail,send_im
from kwippy.views.main import get_display_name
from kwippy.views.mykwips import follow_user_nomail
from kwippy.views.views import queryset_to_csv
from django.views.generic.simple import direct_to_template, redirect_to
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.comments.views.comments import post_comment
from django.core.cache import cache
from django.conf import settings
import datetime
import pdb,os,random,sha

def format_it(data):
    ret_str=data
    if(data.count('\n')>settings.MAX_LINE_BREAKS):
        count = 0
        for ch in data:
            if ch=='\n':
                count=count+1
                if count>settings.MAX_LINE_BREAKS:
                     ret_str=ret_str + " ..."
                     break
                ret_str=ret_str+ch
    elif(len(data)>settings.MAX_STR_LENGTH):
        ret_str = data[:settings.MAX_STR_LENGTH]
        ret_str = ret_str[:ret_str.rfind(' ')]
        ret_str = ret_str + " ..."
    else:
        ret_str = data
    return ret_str

def my_post_comment(request):
    referer = request.META.get('HTTP_REFERER', '')
    if not request.POST.has_key('preview'):
        response = post_comment(request,next=referer)
        curr_user = get_object_or_404(User, username=request.user)
        up = get_object_or_404(User_Profile, user=request.user)
        up.comment_count = up.comment_count+1
        up.save()
        content_type_id=request.POST['content_type']
        object_id=request.POST['object_pk']
        quip = get_object_or_404(Quip,id=int(object_id))
        quip.comment_count = quip.comment_count + 1 # incremnt comment count
        quip.last_comment_at=datetime.datetime.now() # last comment time updated
        quip.save()
        cache_key = '%s_quip%s' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,object_id,)
        cache.delete(cache_key)
	cache_key = '%s_activekwip' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,)
        cache.delete(cache_key)
        obj_user = quip.account.user
        text = request.POST['comment']
        subscribe_comments = request.POST.get('subscribe_comments', False)
        if subscribe_comments:
            follow_comments(request, quip.id)
        timestamp = quip.created_at.strftime("%Y/%b/%d/%H%M%S")
        link = str(obj_user.username)+'/kwips/'+timestamp.lower()+'/?type=comment&src=mail'	    
        #link = str(request['url'][1:])
        params_for_mail = {'#_1':obj_user.username,'#_2':curr_user.username,'#_3':request.POST['comment'],'#_4':link,'#_5':datetime.datetime.now().ctime()}
        if curr_user != obj_user:                
            send_mail(str(obj_user.email),'kwippy <support@kwippy.com>','comment',params_for_mail)
            params_for_mail['#_4'] = params_for_mail['#_4'].replace('mail','im')
            send_im(obj_user,'comment',params_for_mail)
        send_anon_comment_emails(quip,curr_user,params_for_mail,link)
        send_comment_emails(quip,curr_user,params_for_mail,link)	    
        return redirect_to(request, referer)
    return post_comment(request,next=referer)

@login_required
def delete_comment(request,comment_id):
    referer = request.META.get('HTTP_REFERER', '')
    comment_for=get_object_or_404(Comment, id=comment_id)
    quip_for=get_object_or_404(Quip,id=comment_for.object_pk)
    if request.user == comment_for.user or request.user == quip_for.account.user:
        comment_for.delete()
	quip_for.comment_count = quip_for.comment_count - 1 
	quip_for.save()
        up = get_object_or_404(User_Profile, user=request.user)
        up.comment_count = up.comment_count-1
        up.save()
    return redirect_to(request, referer)

@login_required
def follow_comments(request, quip_id):
    #referer = request.META.get('HTTP_REFERER', '')
    user = get_object_or_404(User, id=request.user.id)    
    quip = get_object_or_404(Quip, id=quip_id)
    if user != quip.account.user:
        comm_foll = Comment_Follower.objects.filter(user=user, quip=quip)
        if not comm_foll:
            cf = Comment_Follower(user=user, quip=quip)
            cf.save()

def anon_follow_comments(user,quip):
    anon_comment_follower = Anon_Comment_Follower(user=user,quip=quip)
    anon_comment_follower.save()
    
@login_required    
def unfollow_comments(request, quip_id):
    referer = request.META.get('HTTP_REFERER', '')
    user = get_object_or_404(User, id=request.user.id)    
    quip = get_object_or_404(Quip, id=quip_id)
    comm_foll = Comment_Follower.objects.filter(user=user, quip=quip)
    timestamp = quip.created_at.strftime("%Y/%b/%d/%H%M%S")
    link = '/'+str(quip.account.user.username)+'/kwips/'+timestamp.lower()	    	        
    if comm_foll:
	comm_foll = comm_foll[0]
	comm_foll.delete()    
    if referer!='':
	return redirect_to(request, referer)
    else:
	return HttpResponseRedirect(link)

def anon_unfollow_comments(request, foll_id):    
    referer = request.META.get('HTTP_REFERER', '')
    comm_foll = Anon_Comment_Follower.objects.filter(id=foll_id)
    if comm_foll:
	comm_foll = comm_foll[0]
        timestamp = comm_foll.quip.created_at.strftime("%Y/%b/%d/%H%M%S")
        link = '/'+str(comm_foll.quip.account.user.username)+'/kwips/'+timestamp.lower()	    	        
	comm_foll.delete()    
    if referer!='':
	return redirect_to(request, referer)
    else:
	return HttpResponseRedirect(link)

def send_anon_comment_emails(quip,curr_user,params_for_mail,link):
    anon_followers = Anon_Comment_Follower.objects.filter(quip=quip).exclude(user=curr_user)
    if anon_followers:
        for foll in anon_followers:
            unfollow_link = 'anon_unfollow_comments/'+str(foll.id)
            params_for_mail['#_6'] = curr_user.username
            params_for_mail['#_1'] = unfollow_link
            inv = Invite.objects.filter(invitee_email=foll.user.email[5:])
            if inv:
                params_for_mail['#_7'] = inv[0].unique_hash
            else:
                params_for_mail['#_7'] = ''
	    send_mail(str(foll.user.email[5:]),'Kwippy <support@kwippy.com>','comment_follower_anon',params_for_mail)

def send_comment_emails(quip,curr_user,params_for_mail,link):    
    users_ids_in_csv = email_ids_of_followers(quip.id,curr_user)        
    if users_ids_in_csv:
	users_list = User.objects.filter(id__in=users_ids_in_csv)    
	unfollow_link = 'unfollow_comments/'+str(quip.id)
	params_for_mail['#_6'] = curr_user.username
	params_for_mail['#_7'] = unfollow_link
	for item in users_list:
	    params_for_mail['#_1'] = get_display_name(item)	    
	    send_mail(str(item.email),'Kwippy <support@kwippy.com>','comment_follower',params_for_mail)
            im_link = link.replace('mail','im')
            params_for_im = {'#_1':get_display_name(curr_user),'#_2':params_for_mail['#_3'],'#_3':im_link,'#_4':curr_user.username}
            send_im(item,'comment_follower',params_for_im)
            cf = get_object_or_404(Comment_Follower,user=item,quip=quip)
            cf.is_active=0
            cf.save()

def send_commentbyanon_emails(quip,curr_user,name,params_for_mail,link):    
    users_ids_in_csv = email_ids_of_followers(quip.id,curr_user)        
    if users_ids_in_csv:
	users_list = User.objects.filter(id__in=users_ids_in_csv)    
	unfollow_link = 'unfollow_comments/'+str(quip.id)
	params_for_mail['#_6'] = unfollow_link
	#params_for_mail['#_7'] = unfollow_link
	for item in users_list:
	    params_for_mail['#_1'] = name
	    send_mail(str(item.email),'Kwippy <support@kwippy.com>','comment_byanon_follower',params_for_mail)
            params_for_im = {'#_1':name,'#_2':quip.original,'#_3':link,'#_4':curr_user.username}  
            send_im(item,'comment_follower',params_for_im)
            cf = get_object_or_404(Comment_Follower,user=item,quip=quip)
            cf.is_active=0
            cf.created_at=datetime.datetime.now()
            cf.save()
            
            
def email_ids_of_followers(quip_id,curr_user):    
    quip = get_object_or_404(Quip, id=quip_id)
    followers_list = Comment_Follower.objects.filter(quip=quip,is_active=1).exclude(user=curr_user)
    if followers_list:	
	return queryset_to_csv(followers_list,'comment_follower')
    else:
	return False
    
@login_required
def favourite_comment(request,comment_id):  
  comment= get_object_or_404(Comment, id=comment_id)
  if request.user.is_authenticated:
    cache_key = '%s_favcount%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,request.user.id,)
    cache.delete(cache_key)
    cache_key = '%s_fav_com%d-%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,request.user.id,int(comment_id),)
    cache.delete(cache_key)
    if not Favourite_Comment.objects.filter(comment=comment,user=request.user):
      fav = Favourite_Comment(user=request.user,comment=comment)
      fav.save()
      if comment.user != request.user:
        quip = get_object_or_404(Quip, id = comment.object_pk)
        timestamp = quip.created_at.strftime("%Y/%b/%d/%H%M%S")
        link = str(quip.account.user.username)+'/kwips/'+timestamp.lower()+'/?type=comment&src=mail#'+comment_id 
        params_for_mail = {'#_1':str(comment.user.username),'#_2':str(request.user.username), '#_3':link}
        send_mail(str(comment.user.email),'kwippy <support@kwippy.com>','favorite_comment',params_for_mail)
        params_for_mail['#_3'] = params_for_mail['#_3'].replace('mail','im')
        send_im(comment.user,'favorite_comment',params_for_mail)
        #up = get_object_or_404(User_Profile, user=request.user)
        #up.fav_count = up.fav_count+1
        #up.save()
      return HttpResponse('Favourited')
    else:
      Favourite_Comment.objects.get(comment=comment,user=request.user).delete()
      #up = get_object_or_404(User_Profile, user=request.user)
      #up.fav_count = up.fav_count-1
      #up.save()
      return HttpResponse('UnFavourited')
  return HttpResponse('oops')

def anon_comment(request):
    if request.META.has_key('HTTP_REFERER'):
        referer = request.META.get('HTTP_REFERER', '')
    else:
        referer = str(followee_username)
    name = request.POST['anon_name']
    comment = request.POST['comment']
    inv_code = request.POST['inv_code']
    content_type_id= request.POST['content_type']
    object_id=request.POST['object_pk']
    if name and comment and inv_code :
        anon_invite = get_object_or_404(Anon_Conversation_Invite, code=inv_code)        
        email = anon_invite.receiver
        # code to create an inactive user
        user = User.objects.filter(email='anon_'+email)
        if not user:
            user=User(username='anon_'+email,email='anon_'+email,password='sha1$fd64a$2d7b3b5d6199ef44a08d56d1f1259019072d2',is_active=0)
            user.save()
            random_hash = sha.new(str(user.email)+str(random.random())).hexdigest()[:10]
            user_profile = User_Profile(user=user,display_name=user.username,hash=random_hash,quip_repeat_total=1,quip_total=1)
            user_profile.save()
            page_setting = PageSetting(user=user)
            page_setting.save()
            not_setting = NotificationSetting(user=user)
            not_setting.save()
            #adding default followee, this should be the one who invited him to conv
            #invitee = anon_invite.sender
            #follow_user_nomail(user,invitee.username,0)
        else:
            user = user[0]
        # code to add comment from that user, ip not being captured        
        content_type_kwip = get_object_or_404(ContentType,name='quip')
        comment = Comment(user=user,content_type=content_type_kwip,object_pk=object_id,comment=comment,is_public=1,site_id=1,valid_rating=0,is_removed=0)
        comment.save()
        quip = get_object_or_404(Quip,id=object_id)
        quip.comment_count+=1 # increment comment count
        quip.last_comment_at=datetime.datetime.now() # last comment time updated
        quip.save()
        cache_key = '%s_quip%s' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,object_id,)
        cache.delete(cache_key)
        obj_user = quip.account.user
        timestamp = quip.created_at.strftime("%Y/%b/%d/%H%M%S")
        link = str(obj_user.username)+'/kwips/'+timestamp.lower()
        subscribe_comments = request.POST.get('subscribe_comments', False)
	if subscribe_comments:
            anon_follow_comments(user, quip)        
        #link = str(request['url'][1:])
        params_for_mail = {'#_1':obj_user.username,'#_2':name, '#_3':format_it(quip.original),'#_4':link,'#_5':datetime.datetime.now().ctime()}
        if user != obj_user:
            send_mail(str(obj_user.email),'kwippy <support@kwippy.com>','comment_anon',params_for_mail)
            send_im(obj_user,'comment',params_for_mail)
        # follow up notifications to users for comment by an anon 
        send_commentbyanon_emails(quip,user,name,params_for_mail,link)
        # follow up notifications to anons for comment by an anon 
        send_anon_comment_emails(quip,user,params_for_mail,link)
        return HttpResponseRedirect(referer)
        # code to add follow up notification settings
    else:
        # flash msg
        return HttpResponseRedirect(referer)
