from django.contrib.auth.models import *
from kwippyproject.kwippy.models.user_profile import User_Profile
from kwippyproject.kwippy.models.theme import Theme
from django import template
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.core.cache import cache
import pdb

register = template.Library()

def do_theme(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return ThemeNode(bits[1])

def theme(parser, token):
    return do_theme(parser, token)

class ThemeNode(Node):
    def __init__(self, var1):
        self.var1 = Variable(var1)

    def __repr__(self):
        return "<ThemeNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        if val1=="everyone":
            return ""
        cache_key = '%s_profilequeryname%s' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,)
        user_profile = cache.get(cache_key)
        if user_profile is None:
            user = User.objects.get(username=val1)
            user_profile = get_object_or_404(User_Profile, user=user)
            cache.set(cache_key, user_profile, 86400)

        if not user_profile.theme_id:
            return ""

        color = user_profile.theme.params.split(",")
        style = '''<style type="text/css"> .left_col a{color:%s;}
        .left_col a:hover{color:%s;text-decoration:underline;}
        .kwipsarea{color:%s;background-color:%s;}
        a.selected:hover {color:%s;}
        a.selected,.link_prev, .link_next  {background-color:%s;color:%s;}
        a.unselected:hover {background-color:%s;color:%s;} 
        a.unselected {background-color:%s;color:%s;} 
        .user_pic_16 {border:1px solid %s;} 
        </style>''' % (color[1],color[1],color[2],color[0],color[1],color[0],color[1],color[0],color[1],color[1],color[0],color[1],)

        return style
        
register.tag('theme',do_theme)
