from kwippy.models.quip import Quip
from kwippy.models.account import Account
from kwippy.models.follower import Follower
from kwippy.models.favourite import Favourite
from kwippy.models.user_profile import User_Profile
from django.template import RequestContext
from django.contrib.comments.models import Comment
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib.auth.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.core.paginator import Paginator
from django import template
from kwippy.views.mykwips import details_for_kwips_page
from django.utils.feedgenerator import Atom1Feed
from django.contrib.syndication.feeds import Feed
from django.contrib.syndication.feeds import FeedDoesNotExist
import pdb

def queryset_to_csv(queryset,type):
    csv = []
    for q in queryset:
        if type=='followers':
            csv.append(int(q.follower.id))
        else:
            csv.append(int(q.followee.id))
    return csv  

def user_search(request,filter):    
    if request.method == "GET" and request.GET.has_key('query') and request.GET['query']!='':
#        paginate_by = 10
        max_page = 10
        page = int(request.GET.get('page',0))
        paginate_by = int(request.GET.get('count',20))
        query = request.GET['query']
        start = page*paginate_by
        result = User_Profile.search.query(query)
        quips = Quip.search.query(query).order_by('-%s' % filter)[start:start+paginate_by]
        no_of_results = len(result)+len(quips)
#       paginator = ObjectPaginator(result, paginate_by)
#       page = int(request.GET.get('page',0)) 
#       result = paginator.get_page(page)
#        return render_to_response('list_pages/search_list.html', {'is_paginated': paginator.pages > 1, 'results_per_page': paginate_by,
#                                  'has_next': paginator.has_next_page(page), 'has_previous': paginator.has_previous_page(page),
#                                  'page': page + 1, 'next': page + 1, 'previous': page - 1, 'pages': paginator.pages,
#                                  'hits' : paginator.hits,'followers_profiles': result,'quips': quip_results,'no_of_results':no_of_results,'query':query}, context_instance=template.RequestContext(request))
#        return render_to_response('list_pages/search_list.html', {'followers_profiles': result,'quips': quip_results,
#                                  'no_of_results':no_of_results,'query':query}, context_instance=template.RequestContext(request))
        fc = 2
        link = "/search/"
        if filter=='created_at':
            fc = 1 
            link = "/search/active/"
        link = "%s?query=%s" % (link,query,)
        login = "kwippy"
        if request.user.is_authenticated():
            login = request.user.username
        return render_to_response('search.html', {'login':login,'link':link,'searched':query,'is_paginated': True, 'results_per_page': paginate_by,
                              'has_next': page<max_page, 'has_previous': page>0,
                              'page': page, 'next': page + 1, 'previous': page - 1, 'pages': [],
                              'hits' : 0,'quips': quips,'users':result,
                              'revision_number': settings.REVISION_NUMBER,'filtercount' : fc}, context_instance=template.RequestContext(request))
    else:
        return render_to_response('list_pages/search_list.html', context_instance=template.RequestContext(request))
        

#def quip_search(request):
    
    #paginate_by = 10
    ##query = request.GET.get('query','')
    #query = request.POST.get('query','')
    #result = Quip.search.query(query)
    #paginator = ObjectPaginator(result, paginate_by)
    #page = int(request.GET.get('page',0)) 
    #result = paginator.get_page(page)
    #return render_to_response('list_pages/search_list.html', {'quips': result,
    #}, context_instance=template.RequestContext(request))
    
#def comment_search(request):
    
    #paginate_by = 10
    #query = request.GET.get('query','')
    #result = Comment.search.query(query)
    #paginator = ObjectPaginator(result, paginate_by)
    #page = int(request.GET.get('page',0)) 
    #result = paginator.get_page(page)
    #return render_to_response('comment_area.html', {'comment_list': result,
    #}, context_instance=template.RequestContext(request))

class SearchFeed(Feed):
    title = "Kwippy search feed"
    link = "http://kwippy.com"
    description = "Kwippy search feed."

    def items(self):
        quips = Quip.search.query(self.request.GET.get("q","")).order_by('-created_at')[0:10]
        return quips

    def item_pubdate(self,item):
        """
        Returns the pubdate for every item in the feed.
        """
        return item.created_at

    def item_author_name(self,item):
        """
        Takes the object returned by get_object() and returns the feed's
        author's name as a normal Python string.
        """
        return item.user.username

class AtomSearchFeed(SearchFeed):
    feed_type = Atom1Feed
    subtitle = SearchFeed.description

