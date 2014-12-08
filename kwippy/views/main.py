from django.db import connection
from django.contrib.auth.models import *
from kwippy.models.quip import Quip
from kwippy.models.rquip import Rquip
from kwippy.models.account import Account
from kwippy.models.favourite import Favourite
from kwippy.models.follower import Follower
from kwippy.models.friend import Friend
from kwippy.models.page_setting import PageSetting
from kwippy.models.user_profile import User_Profile
from kwippy.models.email_account import Email_Account
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from kwippy.models.invite import Invite
from kwippy.models.random_user import Random_User
from kwippy.models.conversation_invite import ConversationInvite
from kwippy.models.anon_conversation_invite import Anon_Conversation_Invite
from console_app.views import generate_invite_code,store_invite_in_db
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.forms.fields import email_re
from django.contrib.comments.models import Comment
from kwippy.views.comm_queue import send_mail,send_im
from django.conf import settings
from django.core.cache import cache
from django.utils import simplejson
import re, random, sha

alnum_re = re.compile(r'^\w+$')

def is_in_group(user,group):
        grp = get_object_or_404(Group, name=group)
        if grp in user.groups.all():
                return True
        else:
                return False

def ireplace(self,old,new,count=0):
	''' Behaves like string.replace(), but does so in a case-insensitive
	fashion. '''
	pattern = re.compile(re.escape(old),re.I)
	return re.sub(pattern,new,self,count)

def get_friends(user):
        user_frenz = Friend.objects.filter(sender=user, status=1) | Friend.objects.filter(receiver=user, status=1)
        friend_ids = []
        for item in user_frenz:
                if item.sender == user:
                        friend_ids.append(int(item.receiver.id))
                else:
                        friend_ids.append(int(item.sender.id))
        return friend_ids

def invite_to_conversation(request):
        user_list = []
        user = request.user
        cache_key = '%s_userfollowerqueryfull%s' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,user.id,)
        req_users_followers = cache.get(cache_key)
        if req_users_followers is None:
            cursor = connection.cursor()
            grp=Group.objects.get(name='team')
            if grp in request.user.groups.all():
                    cursor.execute("select auth_user.id from auth_user,kwippy_follower where kwippy_follower.follower_id=auth_user.id and kwippy_follower.followee_id=3 order by auth_user.username")
            else:
                    cursor.execute("select auth_user.id from auth_user,kwippy_follower where kwippy_follower.follower_id=auth_user.id and kwippy_follower.followee_id=%s order by auth_user.username",(user.id,))
            req_users_followers = cursor.fetchall()
            cache.set(cache_key,req_users_followers,14400)
	friend_list = get_friends(user)
	#followers_ids = [item[0] for item in cursor.fetchall()]
        for item in req_users_followers:                
                user = get_object_or_404(User, id = int(item[0]))
                image_path = return_user_image(int(item[0]),'follower')
                if int(user.id) not in friend_list:
                        user_list.append({'user_name':str(user.username),'user_id':int(user.id),'image_path':image_path,'is_friend':False})
                else:
                        user_list.append({'user_name':str(user.username),'user_id':int(user.id),'image_path':image_path,'is_friend':True})
	json = simplejson.dumps(user_list)
        cursor.close()
        return HttpResponse(json,mimetype='application/json')
        #return HttpResponse('%s' % users_followers)                   

def follow_tweople(request):
    username = request.POST.get('username', False)
    registered_list = request.POST['registered_list']
    new_list = registered_list.split(',')
    user = get_object_or_404(User, username=str(username))      
    for item in new_list:
        followee_user = get_object_or_404(User, username=str(item))
        if not Follower.objects.filter(follower=user,followee=followee_user):
            follow = Follower(follower=user,followee=followee_user)
            follow.save()
            params_for_mail = {'#_1':user.username,'#_2':followee_user.username, '#_3':user.username}
            send_mail(str(followee_user.email),'kwippy <support@kwippy.com>','follower',params_for_mail)
            send_im(followee_user,'follower',params_for_mail)            
    return HttpResponse('done')
    
def checkusername(request):
	username = request.POST.get('username', False)    
	if username:
		if len(username)>=3 and len(username)<=18 :
			if alnum_re.search(username):
				u = User.objects.filter(username=username).count()
				if u != 0:
					res = "Already In Use"
				else:
					res = "great username :)"
			else:                
				res = "Special Characters not allowed"
		else:
			res = "Username should have minimum 3 characters and maximum 18 characters"
	else:
        
		res = "Username cannot be blank"
    
	return HttpResponse('%s' % res)

def checkemail(request):        
    email = request.POST.get('email', False)
    if email:
        if email_re.search(email):
            u = User.objects.filter(email=email).count()
            if u != 0:
                res = "Already In Use"
            else:
                res = "Ok"
        else:
            res = "Invalid Email Address"
    else:
   	res = "Email address cannot be blank"            

    return HttpResponse('%s' % res)

def checkpassword1(request):        
    password1 = request.POST.get('password1', False)
    if password1:
        if len(password1)>=5:
            res = "OK"
        else:
            res = "password should contain minimum 5 characters"
    else:
        res = "password cannot be blank"

    return HttpResponse('%s' % res)


def checkpassword2(request):
    password1 = request.POST.get('password1', False)
    password2 = request.POST.get('password2', False)
    if password1 and password2:
        if password2==password1:            
            res = "OK"
        else:
            res = "passwords don't match"
    else:
        res = "password cannot be blank"
    
    return HttpResponse('%s' % res)

def get_display_name(user):    
    disp_name = user.get_profile().display_name
    if disp_name:        
        return disp_name
    else:
        return str(user.username)

@login_required    
def invite_user(request):
	if request.method == "POST":
		invite = Invite.objects.filter(invitee_email=request.POST.get('e-mail'))
		if invite and invite[0].status==2:
			user=get_object_or_404(User, email=request.POST.get('e-mail'))
			url=settings.SITE+"/"+user.username				
			request.session['flash'] = "\""+request.POST.get('e-mail')+"\""+" is already registered as "+user.username+" :)"
		else:
			invite_hash = generate_invite_code( request.POST.get('e-mail'),request.user.email)      
			store_invite_in_db(request, invite_hash,'friend')
			request.session['flash'] = "An invite was sent to "+ str(request.POST.get('e-mail')) +" successfully !!"
        return HttpResponseRedirect('/'+request.user.username+'/')	
    

def kwip_count(user):
        up = get_object_or_404(User_Profile, user=user)
	show_repeat = get_object_or_404(PageSetting, user=user).show_repeat
        if show_repeat:
            count = up.quip_repeat_total
        else:
            count = up.quip_total
	return count
	
def comment_count(user):
        up = get_object_or_404(User_Profile, user=user)
	return up.comment_count

def favorite_count(user):
	up = get_object_or_404(User_Profile, user=user)
        return up.fav_count


def invite_to_talk(request):
        if request.META.has_key('HTTP_REFERER'):
            referer = request.META.get('HTTP_REFERER', '')
        else:
            referer = str(followee_username)        
        user = request.user
        count = 0
        quip = get_object_or_404(Quip, id=int(request.POST['qpid']))
        timestamp = quip.created_at.strftime("%Y/%b/%d/%H%M%S")
        link = str(quip.account.user.username)+'/kwips/'+timestamp.lower()
        for item in request.POST:
                if item != 'qpid':
                        split = item.split('_')
                        if split[0] == 'email':
                            code = sha.new(split[1]+user.email+str(random.random())).hexdigest()[:10]
                            anon_conv_invite = Anon_Conversation_Invite(quip=quip,sender=user,receiver=request.POST['email_'+split[1]],code=code)
                            anon_conv_invite.save()
                            invite = Invite(invitee_email=request.POST['email_'+split[1]],user=user,invite_type=5,unique_hash=code)
                            invite.save()
                            params_for_mail = {'#_2':user.username, '#_1':link+'/?type=anoninvite2talk&src=mail&inv_code='+code}
                            send_mail(str(request.POST['email_'+split[1]]),'kwippy <support@kwippy.com>','invite_to_talk_anon',params_for_mail)                            
                        else:
                            if split[0] != 'non' and split[0] !='select':
                                    receiver = get_object_or_404(User, id=int(split[1]))
                                    if not ConversationInvite.objects.filter(quip=quip,receiver=receiver):
                                        if not Comment.objects.filter(object_pk=quip.id,user=receiver):
                                            if quip.user_id != receiver.id:
                                                conv_invite = ConversationInvite(quip=quip,receiver=receiver,sender=request.user,comment_count=quip.comment_count)
                                                conv_invite.save()
                                                params_for_mail = {'#_1':receiver.username,'#_2':request.user.username, '#_3':link+'/?type=invite2talk&src=mail'}
                                                send_mail(str(receiver.email),'kwippy <support@kwippy.com>','invite_to_talk',params_for_mail)
                                                params_for_mail['#_3'] = params_for_mail['#_3'].replace('mail','im')
                                                send_im(receiver,'invite_to_talk',params_for_mail)            
                                                count = count + 1
        if quip.user_id != request.user.id:
            params_for_mail = {'#_1':quip.user.username,'#_2':request.user.username, '#_3':link+'/?type=notifyinvite2talk&src=mail'}
            send_mail(str(quip.user.email),'kwippy <support@kwippy.com>','notify_invite_to_talk',params_for_mail)
            params_for_mail['#_3'] = params_for_mail['#_3'].replace('mail','im')
            send_im(quip.user,'notify_invite_to_talk',params_for_mail)
        request.session['flash'] = "Invites to join conversation sent"
        return HttpResponseRedirect(referer)

def return_user_image(user_id,type_of_pic):
        user = get_object_or_404(User, id=user_id)
        user_profile = get_object_or_404(User_Profile, user=user)
            
        s3_path = "http://s3.amazonaws.com/"+settings.BUCKET_NAME+'/'
        if user_profile:
            if user_profile.media_processed==2:                
                # return path for pic for follower and followee sections                    
                image_path = s3_path + str(user_id) +"."+ str(user_profile.picture_ver) + '.'+type_of_pic                
            else:
                gender = user_profile.gender
                if gender:
                    if gender==1:
                        image_path = s3_path+"dude.0."+type_of_pic
                    elif gender==2:
                        image_path = s3_path+"duddette.0."+type_of_pic
                else:#unisex image
                    image_path = s3_path+"unisex.0."+type_of_pic                
            return image_path


def random_users(count):
    rnum = random.randint(1,25)
    user_profiles = Random_User.objects.filter(set_id=rnum)
    #Random_User
    #user_profiles = User_Profile.objects.filter(media_processed=2).exclude(id__in=[53,1])
    #user_profiles_list = list(user_profiles)[:90]
    items = []
    for profile in user_profiles:
        items.append(int(profile.user_id))
    #random.shuffle(items)
    return items[:count]
   
def rss_users():
    rss_users = User.objects.filter(id__in=[7377,7382,7400])
    return rss_users

def active_users(count):
    cursor = connection.cursor()
    #cursor.execute("select max(id) from comments_comment where user_id <> 53 group by user_id order by max(submit_date) desc limit 9;")
    #cursor.execute("select max(comments_comment.id) from comments_comment inner join kwippy_quip on kwippy_quip.id=comments_comment.object_id where comments_comment.user_id <> 53 group by comments_comment.user_id order by max(submit_date) desc limit 9;")
    cursor.execute("select id from kwippy_quip where comment_count> 0 and id > 1500000 order by last_comment_at desc limit 9;")
    kwip_ids = [item[0] for item in cursor.fetchall()]
    active_kwips = Quip.objects.filter(id__in=kwip_ids).order_by('-last_comment_at')
    list = []
    for kwip in active_kwips:
        dict = {}
        dict['kwip'] = kwip
        comments = Comment.objects.filter(object_pk=kwip.id).order_by('-submit_date')
        if comments:
            dict['comment'] = comments[:1][0]
            list.append(dict)
    cursor.close()
    return list

def activate_secondary_email(request, activation_code):
        email_acc = get_object_or_404(Email_Account,code=activation_code)
        email_acc.status = 1
        email_acc.save()
        request.session['flash'] = "secondary email account verified"
        return HttpResponseRedirect('/'+request.user.username+'/dashboard/account/')

def resend_activate_secondary_email(request):
        user = request.user
        email_acc = get_object_or_404(Email_Account,user=user)
        send_mail(str(email_acc.email),'support@kwippy.com','email_activation',{'#_1':user.username,'#_2':email_acc.code})
        request.session['flash'] = "verification email sent"
        return HttpResponseRedirect('/'+request.user.username+'/dashboard/account/')
