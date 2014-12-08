from kwippyproject.kwippy.models.quip import Quip
from kwippyproject.kwippy.models.comment_follower import Comment_Follower
from django.contrib.auth.models import User
from django.conf import settings
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.core.cache import cache
import pdb

register = template.Library()

def do_show_comment_subscription(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return CommentSubscriptionNode(bits[1], bits[2])

def show_comment_subscription(parser, token):
    return do_show_comment_subscription(parser, token)

class CommentSubscriptionNode(Node):
    def __init__(self, var1, var2):
        self.var1 = Variable(var1)
	self.var2 = Variable(var2)
        
    def __repr__(self):
        return "<CommentSubscriptionNode>"

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
            cache.set(cache_key,user,86400)
        
        comm_follow = Comment_Follower.objects.filter(user=user, quip=quip)
	if user!=quip.user:
	    if not comm_follow:
		html = "<label class=\"float_left\"><input type=\"checkbox\" class=\"float_left checkbox\" id=\"subscribe_comments\" value=\"true\" checked=\"true\" name=\"subscribe_comments\"/> notify on follow-up comments</label>"
		return html
	    else:
		html = "<h3 class=\"float_left\">email notifications are being sent on new comments - &nbsp;</h3> <a class=\"float_left\"  href=\"/unfollow_comments/"+str(quip.id)+"\"> Unsubscribe</a>"
		return html
	else:
	    return ""
        
register.tag('show_comment_subscription',do_show_comment_subscription)
