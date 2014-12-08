import sha, random,pdb,os,datetime, re,time
from django.conf import settings
from django import oldforms, template, http
from kwippy.views.comm_queue import send_mail, comm_queue, send_im
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth.__init__ import login
from django.contrib.comments.models import Comment
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import ObjectPaginator, InvalidPage
from kwippy.models.quip import Quip
from kwippy.models.account import Account
from kwippy.models.account_delete import AccountDelete
from kwippy.models.user_profile import User_Profile
from kwippyproject.comm_queue_app.models import Commd
from django.contrib.auth.models import *

def new_users(request,year=0,month=0,day=0):
    now = datetime.datetime.now()
    new_users = User.objects.filter(date_joined__gte=now.date())
    return render_to_response("console/new_users.html",{'new_users':new_users})

def inactive_users(request):
    #if request.user.g
    from django.db import connection
    cursor = connection.cursor()   
    cursor.execute("select * from auth_user where id not in (select distinct(user_id) from comments_comment) limit 250")
    user_ids = [int(item[0]) for item in cursor.fetchall()]
    zero_comment_users = User.objects.filter(id__in=user_ids).order_by('-last_login')
    return render_to_response("console/inactive_users.html", {'zero_comment_users': zero_comment_users,},context_instance=template.RequestContext(request))
    #else:
    #return HttpResponseRedirect('/'+request.user.username+'/')

@login_required
def toppers(request):
    grp=Group.objects.get(name='team')
    if grp in request.user.groups.all():
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("select count(*),user_id from comments_comment where user_id not in (3,4,6,53) group by user_id order by count(*) desc limit 25;")
        comment_toppers = cursor.fetchall()
        cursor.execute("select count(*),user_id from kwippy_favourite where user_id not in (3,4,6,53) group by user_id order by count(*) desc limit 25;")
        favorite_toppers =  cursor.fetchall()
        cursor.execute("select count(*),user_id from kwippy_quip where repeat_id in (0,id) and user_id not in (-1,3,4,6,53) group by user_id order by count(*) desc limit 25;")
        kwip_toppers =  cursor.fetchall()        
        return render_to_response("console/toppers.html", {'comment_toppers': comment_toppers,'kwip_toppers':kwip_toppers,'favorite_toppers':favorite_toppers},context_instance=template.RequestContext(request))
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')


