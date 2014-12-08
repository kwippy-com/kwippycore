from kwippyproject.kwippy.models.friend import Friend
from django.contrib.auth.models import User
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
import pdb

register = template.Library()

def do_show_is_friend(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return IsfriendNode(bits[1], bits[2])

def show_is_friend(parser, token):
    return do_show_is_friend(parser, token)

class IsfriendNode(Node):
    def __init__(self, var1, var2):
        self.var1 = Variable(var1)
	self.var2 = Variable(var2)
        
    def __repr__(self):
        return "<IsfriendNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        try:
            val2 = self.var2.resolve(context)
        except VariableDoesNotExist:
            val2 = None
        user_1 = get_object_or_404(User, username = val1)
        user_2 = get_object_or_404(User, username = val2)	
        friendship = Friend.objects.filter(sender=user_1, receiver=user_2) | Friend.objects.filter(sender=user_2, receiver=user_1)
	if friendship:
            friendship = friendship[0]
            if friendship.status == 1:
		html = "<div><div style=\"float:left;width:75px;\"><img src=\"/images/icons/minus.gif\"> </div><div style=\"float:left;\"><a align=\"left\" href=\"/friendships/remove/"+(str(val2))+"/\" > remove as friend</a></div></div>"
		html = html + " <div class=\"clear\"></div>"
               # html =  "<a align=\"left\" href=\"/friendships/remove/"+(str(val2))+"/\" ><img class=\"go_icon\" title=\"remove as friend\" src=\"/images/icons/minus.gif\" />remove as friend</a> "
            else:
                if Friend.objects.filter(sender=user_1, receiver=user_2):
                    html = "<i>friend request pending</i>"
                else:
			html = "<div><div style=\"float:left;width:75px;\"><img class=\"go_icon\" title=\"add as friend\" src=\"/images/icons/plus.gif\"></div><div style=\"float:left;\"><a align=\"left\" href=\"/friendships/add/"+(str(val2))+"/\" > add as a friend</div></div>"
			html = html + " <div class=\"clear\"></div>"
		
                   # html =  "<a align=\"left\" href=\"/friendships/add/"+(str(val2))+"/\" ><img class=\"go_icon\" title=\"add as friend\" src=\"/images/icons/plus.gif\" />add as friend</a> "
	else:
		html = "<div><div style=\"float:left;width:75px;\"><img class=\"go_icon\" title=\"add as friend\" src=\"/images/icons/plus.gif\"></div><div style=\"float:left;\"><a align=\"left\" href=\"/friendships/add/"+(str(val2))+"/\" > add as a friend</div></div>"
		html = html + " <div class=\"clear\"></div>"
        #html =  "<a align=\"left\" href=\"/friendships/add/"+(str(val2))+"/\" ><img class=\"go_icon\" title=\"add as friend\" src=\"/images/icons/plus.gif\" />add as  friend</a> "
        return html

        
register.tag('show_is_friend',do_show_is_friend)
