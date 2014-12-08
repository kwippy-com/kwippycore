from kwippyproject.kwippy.models.quip import Quip
from kwippy.models.user_profile import User_Profile
from django.contrib.auth.models import User
from django import template
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.core.cache import cache

register = template.Library()

def do_formatdisplayname(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return FormatDisplayNameNode(bits[1])

def formatdisplayname(parser, token):
    return do_formatdisplayname(parser, token)

class FormatDisplayNameNode(Node):
    def __init__(self, var1):
        self.var1 = Variable(var1)
        
    def __repr__(self):
        return "<FormatDisplayNameNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        
        cache_key = '%s_user%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,)
        user = cache.get(cache_key)
        if user is None:
            user = get_object_or_404(User, id=val1)
            cache.set(cache_key,user,86400)
            
        if user:
            cache_key = '%s_profilequery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,user.id,)
            user_profile = cache.get(cache_key)
            if user_profile is None:
                user_profile = get_object_or_404(User_Profile,user=user)
                cache.set(cache_key, user_profile,86400)
                
            if user_profile and user_profile.display_name:
                display_name = user_profile.display_name
            else:
                display_name = user.username
            return display_name
        
register.tag('formatdisplayname',do_formatdisplayname)
