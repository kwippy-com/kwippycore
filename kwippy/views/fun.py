from __future__ import division
import os,pdb, datetime
from django import template, http
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from kwippy.views.main import get_display_name
from kwippy.views.views import queryset_to_csv
from kwippy.models.account import Account
from kwippy.models.quip import Quip
from kwippyproject.kwippy.models.invite import Invite
from kwippy.models.favourite import Favourite
from kwippyproject.kwippy.models.user_profile import User_Profile
from django.core.cache import cache
from django.contrib.auth.models import User
from kwippy.views.main import comment_count,kwip_count
from django.db import connection


@login_required
def stats(request,user_login):
    referer = request.META['PATH_INFO']
    if str(referer.split('/')[1])!=str(request.user.username):
        return HttpResponseRedirect('/'+str(request.user.username)+'/dashboard/')
    total_comments = comment_count(request.user)
    #total_kwips_commented = Comment
    quip_count = kwip_count(request.user)
    favs_count = Favourite.objects.filter(user=request.user).count()
    days_since_joined = (datetime.datetime.now() - request.user.date_joined).days
    average_kwips_day = quip_count/days_since_joined
    average_comments_day = total_comments/days_since_joined
    new_data, errors = {}, {}
    user_profile = get_object_or_404(User_Profile, user=int(request.user.id))
    displayname = get_display_name(request.user)
    accounts = Account.objects.filter(user=request.user)
    totalcount = 0
    plist = ''
    per = ''
    for a in accounts:
        quip = Quip.objects.filter(account=a)
        if len(quip)!=0:
            totalcount=totalcount+len(quip)
            plist=plist+'|'+a.get_provider_display()+"("+str(len(quip))+")"
    for a in accounts:
        quip = Quip.objects.filter(account=a)
        if len(quip)!=0:
            per=per+","+str((len(quip)*100)/totalcount)
    cursor = connection.cursor()
    cursor.execute("select DATE(kwippy_quip.created_at),count(1) from kwippy_quip,kwippy_account where kwippy_account.user_id=%d and kwippy_quip.account_id=kwippy_account.id and DATEDIFF(NOW(),kwippy_quip.created_at)<100  GROUP BY 1 ORDER BY 1" % (int(request.user.id),))
    pday = ""
    max_count = 0
    for item in cursor.fetchall():
        if item[1]>max_count:
            max_count=item[1]
        pday=pday+","+str(item[1])
    limit = "0,"+str(max_count+10)
    limit2 = "0:|0|"+str(max_count)+"|"+str(max_count+10)+"|"
    cursor.execute("select count(*) from django_comments where object_pk in (select id from kwippy_quip where user_id=%d)" % (int(request.user.id),))
    comments_on_kwips = cursor.fetchall()[0][0]
    cursor.execute("select count(*) from kwippy_favourite where quip_id in (select id from kwippy_quip where user_id=%d)" % (int(request.user.id),))
    bookmarks_on_kwips = cursor.fetchall()[0][0]
    avg_kwip = "%10.*f" % (2,average_kwips_day)
    avg_comment = "%10.*f" % (2,average_comments_day)
    cursor.close()
    return render_to_response('dashboard/dashboard_stats.html', { 'displayname':displayname,'user_profile': user_profile,'per':per[1:],'list':plist[1:],'pday':pday[1:],'limit':limit, 'limit2' : limit2,'total_comments':total_comments,'kwip_count':quip_count,'favs_count':favs_count,'average_kwips_day':avg_kwip,'average_comments_day':avg_comment,'comments_on_kwips':comments_on_kwips,'bookmarks_on_kwips':bookmarks_on_kwips},context_instance=template.RequestContext(request))
