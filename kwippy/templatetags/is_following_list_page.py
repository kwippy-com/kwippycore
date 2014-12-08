from kwippyproject.kwippy.models.follower import Follower
from django.contrib.auth.models import User
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.conf import settings

register = template.Library()

def do_show_is_following_list(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return IsFollowingListNode(bits[1], bits[2])

def show_is_following_list(parser, token):
    return do_show_is_following(parser, token)

def isfollowing(follower,followee):
    f = Follower.objects.filter(follower=follower,followee=followee)
    if f:
        return True
    else:
        return False
    
class IsFollowingListNode(Node):
    def __init__(self, var1, var2):
        self.var1 = Variable(var1)
	self.var2 = Variable(var2)
        
    def __repr__(self):
        return "<IsFollowingListNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        try:
            val2 = self.var2.resolve(context)
        except VariableDoesNotExist:
            val2 = None
        
        user_1 = get_object_or_404(User, id=val1)
        user_2 = get_object_or_404(User, id=val2)
        following_2 = isfollowing(user_1,user_2)
	if user_1!=user_2:
	    if not following_2:
		html="<a href=\"/follow/"+user_2.username+"?to_do=follow\" id=\"follow\" > <span class=\"follow_icon\"><img src=\"/images/icons/plus.gif\" /></span> follow </a>"
		return html
	    else:
		html="<span class=\"grey_bg\">you are already following</span>"
		return html
	else:
	    return "yourself"
        
register.tag('show_is_following_list',do_show_is_following_list)
