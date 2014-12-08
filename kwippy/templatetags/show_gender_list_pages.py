from django.contrib.auth.models import *
from kwippyproject.kwippy.models.user_profile import User_Profile
from django import template
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable

register = template.Library()

def do_show_gender(parser, token):    
    bits = list(token.split_contents())
    nodelist = NodeList()    
    return ShowGenderNode(bits[1])

def show_follower_pic(parser, token):
    return do_show_gender(parser, token)
    
class ShowGenderNode(Node):
    def __init__(self, var1):
        self.var1 = Variable(var1)        
        
    def __repr__(self):
        return "<ShowGenderNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None        
        user_profile= get_object_or_404(User_Profile, id=val1)
        gender = user_profile.get_gender_display()
        return gender
        
register.tag('show_gender',do_show_gender)
