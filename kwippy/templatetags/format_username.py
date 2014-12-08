from kwippyproject.kwippy.models.quip import Quip
from django.contrib.auth.models import User
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.conf import settings
from django.core.cache import cache

register = template.Library()

def do_formatusername(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return FormatUsernameNode(bits[1])

def formatusername(parser, token):
    return do_formatusername(parser, token)

class FormatUsernameNode(Node):
    def __init__(self, var1):
        self.var1 = Variable(var1)
        
    def __repr__(self):
        return "<FormatUsernameNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        if val1 is None:
            return "None"
	else:
            cache_key = '%s_user%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,)
            user = cache.get(cache_key)
            if user is None:
                user = get_object_or_404(User, id=val1)
                cache.set(cache_key,user,86400)
            return user.username

register.tag('formatusername',do_formatusername)
