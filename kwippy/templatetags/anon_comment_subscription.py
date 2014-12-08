from kwippyproject.kwippy.models.quip import Quip
from kwippyproject.kwippy.models.anon_comment_follower import Anon_Comment_Follower
from kwippyproject.kwippy.models.anon_conversation_invite import Anon_Conversation_Invite
from django.contrib.auth.models import User
from django.conf import settings
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.core.cache import cache
import pdb

register = template.Library()

def do_show_anon_comment_subscription(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return AnonCommentSubscriptionNode(bits[1], bits[2])

def show_anoncomment_subscription(parser, token):
    return do_show_anon_comment_subscription(parser, token)

class AnonCommentSubscriptionNode(Node):
    def __init__(self, var1, var2):
        self.var1 = Variable(var1)
	self.var2 = Variable(var2)
        
    def __repr__(self):
        return "<AnonCommentSubscriptionNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        try:
            val2 = self.var2.resolve(context)
        except VariableDoesNotExist:
            val2 = None

        #cache_key = '%s_user%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,)
        #user = cache.get(cache_key)
        #if user is None:
        #    user = get_object_or_404(User, id=val1)
        #    cache.set(cache_key,user,86400)
	anon_comment_invite = get_object_or_404(Anon_Conversation_Invite, code=val1)
	user = get_object_or_404(User, email='anon_'+anon_comment_invite.receiver)
        
        cache_key = '%s_quip%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val2,)
        quip = cache.get(cache_key)
        if quip is None:
            quip = get_object_or_404(Quip, id=val2)
            cache.set(cache_key,user,86400)
        
        comm_follow = Anon_Comment_Follower.objects.filter(user=user, quip=quip)
	if user!=quip.account.user:
	    if not comm_follow:
		html = "<label class=\"float_left\"><input type=\"checkbox\" class=\"float_left checkbox\" id=\"subscribe_comments\" value=\"true\" checked=\"true\" name=\"subscribe_comments\"/> notify on follow-up comments</label>"
		return html
	    else:
		html = "<h3 class=\"float_left\">email notifications are being sent on new comments - &nbsp;</h3> <a class=\"float_left\"  href=\"/anon_unfollow_comments/"+str(comm_follow[0].id)+"\"> Unsubscribe</a>"
		return html
	else:
	    return ""
        
register.tag('show_anon_comment_subscription',do_show_anon_comment_subscription)
