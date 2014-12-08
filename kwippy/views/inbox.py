from django.conf import settings
from kwippyproject.kwippy.models.list_filter import List_Filter
from kwippyproject.kwippy.models.spam_filter import Spam_Filter
from kwippyproject.kwippy.models.sent_filter import Sent_Filter
from kwippyproject.kwippy.views.mykwips import details_for_kwips_page
from django.core.paginator import Paginator
from kwippy.views.main import get_display_name, comment_count, kwip_count
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django import template, http
from django.http import HttpResponse, HttpResponseRedirect


@login_required
def list(request,user_login):
    referer = request.META['PATH_INFO']
    if str(referer.split('/')[1])!=str(request.user.username):
        return HttpResponseRedirect('/'+str(request.user.username)+'/messages/inbox/')
    page = int(request.GET.get('page',1))
    messages = List_Filter.objects.filter(receiver_user=int(request.user.id)).order_by('-created_at')
    link = request.user.username+'/inbox/'
    dict = details_for_kwips_page(request,request.user.username)
    paginator = Paginator(messages,20)
    pmessages_page = paginator.page(page)
    pmessages = pmessages_page.object_list
    unread_incoming_msgs = List_Filter.objects.filter(receiver_user=int(request.user.id), status=0).count()
    return render_to_response('messages/inbox.html', {'is_paginated': paginator.num_pages > 1, 'results_per_page': 20,
                              'has_next': pmessages_page.has_next(), 'has_previous': pmessages_page.has_previous(),
                              'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': 0,
                              'hits' : 0, 'login': request.user.username,'messages': pmessages,
                              'type': 'list','dict':dict,'link':link,'unread_incoming_msgs':unread_incoming_msgs,
                              'revision_number': settings.REVISION_NUMBER,}, context_instance=template.RequestContext(request))

@login_required
def sent(request,user_login):
    referer = request.META['PATH_INFO']
    if str(referer.split('/')[1])!=str(request.user.username):
        return HttpResponseRedirect('/'+str(request.user.username)+'/messages/outbox/')
    page = int(request.GET.get('page',1))
    messages = Sent_Filter.objects.filter(sender_user=int(request.user.id)).order_by('-created_at')
    link = request.user.username+'/inbox/sent/'
    dict = details_for_kwips_page(request,request.user.username)
    paginator = Paginator(messages,20)
    pmessages_page = paginator.page(page)
    pmessages = pmessages_page.object_list
    unread_incoming_msgs = List_Filter.objects.filter(receiver_user=int(request.user.id), status=0).count()
    return render_to_response('messages/outbox.html', {'is_paginated': paginator.num_pages > 1, 'results_per_page': 20,
                              'has_next': pmessages_page.has_next(), 'has_previous': pmessages_page.has_previous(),
                              'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': 0,
                              'hits' : 0, 'login': request.user.username,'messages': pmessages,
                              'type': 'sent','dict':dict,'link':link,'unread_incoming_msgs':unread_incoming_msgs,
                              'kwip_count':kwip_count(dict['user']),'comment_count':comment_count(dict['user']),
                              'revision_number': settings.REVISION_NUMBER,}, context_instance=template.RequestContext(request))

@login_required
def spam(request,user_login):
    page = int(request.GET.get('page',1))
    messages = Spam_Filter.objects.filter(sender_user=int(request.user.id)).order_by('-created_at')
    link = request.user.username+'/inbox/spam/'
    dict = details_for_kwips_page(request,request.user.username)
    paginator = ObjectPaginator(messages,20)
    pmessages_page = paginator.page(page)
    return render_to_response('inbox.html', {'is_paginated': paginator.num_pages > 1, 'results_per_page': 20,
                              'has_next': pmessages_page.has_next(), 'has_previous': pmessages_page.has_previous(),
                              'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': 0,
                              'hits' : 0, 'login': request.user.username,'messages': pmessages,
                              'type': 'spam','dict':dict,'link':link,
                              'kwip_count':kwip_count(dict['user']),'comment_count':comment_count(dict['user']),
                              'revision_number': settings.REVISION_NUMBER,}, context_instance=template.RequestContext(request))
