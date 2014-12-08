from kwippyproject.kwippy.models.quip import Quip
from kwippyproject.kwippy.models.comment_follower import Comment_Follower
from django.contrib.auth.models import User
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.conf import settings
from django.core.cache import cache
import pdb

register = template.Library()

def do_show_is_following_comments(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return IsFollowingCommentsNode(bits[1], bits[2])

def show_is_following_comments(parser, token):
    return do_show_is_following_comments(parser, token)

class IsFollowingCommentsNode(Node):
    def __init__(self, var1, var2):
        self.var1 = Variable(var1)
	self.var2 = Variable(var2)
        
    def __repr__(self):
        return "<IsFollowingCommingNode>"

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
        user = cache.get(cache_key)
        if user is None:
            user = get_object_or_404(User, id=val1)
            cache.set(cache_key,user,86400)
        
        cache_key = '%s_quip%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val2,)
        quip = cache.get(cache_key)
        if quip is None:
            quip = get_object_or_404(Quip, id=val2)	
            cache.set(cache_key,quip,86400)
        
        cf = Comment_Follower.objects.filter(user=user, quip = quip)
	if cf and user!=quip.account.user:
	    html = "<form method=""post"" name=""follow_comments"" action=""/follow_comments/"+str(quip.id)+"/><div align=""right""><input type=""checkbox"" checked=""true""  onClick=""document.follow_comments.submit();"" id=""follow_comments_"""+str(quip.id)+"><h3>subscribe comments</h3></div></form>"    	    
	else:
	    html = "<form method=""post"" name=""follow_comments"" action=""/follow_comments/"+str(quip.id)+"/><div align=""right""><input type=""checkbox"" onClick=""document.follow_comments.submit();"" id=""follow_comments_"""+str(quip.id)+"><h3>subscribe comments</h3></div></form>"	
	return html
        
register.tag('show_is_following_comments',do_show_is_following_comments)