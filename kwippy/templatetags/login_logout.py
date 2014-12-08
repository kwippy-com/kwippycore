from kwippyproject.kwippy.models.list_filter import List_Filter
from django.contrib.auth.models import User
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.core.cache import cache
from django.conf import settings
import pdb

register = template.Library()

def do_show_login_logout(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return LoginLogoutNode(bits[1])

def show_login_logout(parser, token):
    return do_show_is_following(parser, token)

    
class LoginLogoutNode(Node):
    def __init__(self, var1):
        self.var1 = Variable(var1)
        
    def __repr__(self):
        return "<LoginLogoutNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None

        user =  get_object_or_404(User, id=val1)  
	if user:
            unread_messages = List_Filter.objects.filter(receiver_user=user, status=0)
	    html = "<span class=float_right>"
            html= html  + "Hi, <a href='/"+user.username+"/'>"+user.username+"</a> | <a href='/"+user.username+"/dashboard/account/stats'>stats</a> | "
            html = html + "<a href='/"+user.username+"/dashboard/'>dashboard</a> | "
            if unread_messages:
                html = html + "<a href='/"+user.username+"/messages/inbox/'><b>messages("+str(unread_messages.count())+")</b></a> | "
            else:
                html = html + "<a href='/"+user.username+"/messages/inbox/'>messages</a> | "	    
            return html + "<a href='/logout/'>logout</a> </span>"
        
register.tag('show_login_logout',do_show_login_logout)
