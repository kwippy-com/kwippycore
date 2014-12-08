from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django import oldforms, template, http
from django.core.paginator import ObjectPaginator, InvalidPage
from django.contrib.auth.decorators import login_required

from kwippy.models.feedback import Feedback
#This piece of code is being written at 1:42 on 8th Mar by MD on his lappy without electricity.

@login_required
def main(request,fb_for='all'):
    if request.user.is_superuser:
        page = int(request.GET.get('page',0))
        paginate_by = 10
        if fb_for=='self':
            feedback =  Feedback.objects.filter(user=request.user).order_by('-created_at')
        elif fb_for=='all':
            feedback = Feedback.objects.all().order_by('-created_at')
        paginator = ObjectPaginator(feedback, paginate_by)    
        feedback = paginator.get_page(page)
        return render_to_response('fb.html', {'is_paginated': paginator.pages > 1, 'results_per_page': paginate_by,
                                'has_next': paginator.has_next_page(page), 'has_previous': paginator.has_previous_page(page),
                                'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': paginator.pages,
                                'hits' : paginator.hits,'quips': feedback,'quips_for': fb_for,},
                                context_instance=template.RequestContext(request))
    else:
        return HttpResponseRedirect('/'+request.user.username+'/')	

#sweating by still coding :)    