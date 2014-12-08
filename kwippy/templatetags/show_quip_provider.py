from kwippyproject.kwippy.models.quip import Quip
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.core.cache import cache
from django.conf import settings
import pdb

register = template.Library()

def do_displayprovider(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return DisplayProviderNode(bits[1])

def displayprovider(parser, token):
    return do_displayprovider(parser, token)

class DisplayProviderNode(Node):
    def __init__(self, var1):
        self.var1 = Variable(var1)
        
    def __repr__(self):
        return "<DisplayProviderNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        cache_key = '%s_quipprovider%s' %(settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1)
        provider = cache.get(cache_key)
        if provider is None:
            quip = get_object_or_404(Quip, id=val1)
            provider = quip.account.get_provider_display()
            cache.set(cache_key, provider, 86400)
        return provider
        
register.tag('displayprovider',do_displayprovider)