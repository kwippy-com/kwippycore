from kwippyproject.kwippy.models.follower import Follower
from django.contrib.auth.models import User
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.core.cache import cache
from django.conf import settings
import pdb

register = template.Library()

def do_show_is_following(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return IsFollowingNode(bits[1], bits[2])

def show_is_following(parser, token):
    return do_show_is_following(parser, token)

def isfollowing(follower,followee):
    f = Follower.objects.filter(follower=follower,followee=followee)
    if f:
        return True
    else:
        return False
    
class IsFollowingNode(Node):
    def __init__(self, var1, var2):
        self.var1 = Variable(var1)
	self.var2 = Variable(var2)
        
    def __repr__(self):
        return "<IsFollowingNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        try:
            val2 = self.var2.resolve(context)
        except VariableDoesNotExist:
            val2 = None
        
        cache_key = '%s_user%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,)
        user_1 = cache.get(cache_key)
        if user_1 is None:
            user_1 = get_object_or_404(User, id=val1)
            cache.set(cache_key,user_1,86400)
        
        cache_key = '%s_user%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,)
        user_2 = cache.get(cache_key)
        if user_2 is None:
            user_2 = get_object_or_404(User, id=val2)
            cache.set(cache_key,user_2,86400)
        
        cache_key = '%s_follow%dto%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,val2,)
        following_2 = cache.get(cache_key)
        if following_2 is None:
            following_2 = isfollowing(user_1,user_2)
            cache.set(cache_key,following_2,86400)
            
        #following_1 = Follower.objects.filter(followee=user_1,follower=user_2)
	if user_1!=user_2:
	    if not following_2:
		html="<a href=\"/follow/"+user_2.username+"?to_do=follow\" id=\"follow\" > <span class=\"follow_icon\"><img src=\"/images/icons/plus.gif\" /></span> follow </a>"
		return html
	    else:
		html="<span class=\"grey_bg\">you are already following</span>"
		return html
	else:
	    return "yourself"
        
register.tag('show_is_following',do_show_is_following)
