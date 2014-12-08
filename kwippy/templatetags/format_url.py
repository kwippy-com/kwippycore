from kwippyproject.kwippy.models.quip import Quip
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.core.cache import cache
from django.conf import settings
import pdb, re

register = template.Library()

regex = re.compile('^.*(https?:\/\/[^\ \s]*).*$')


def do_formaturl(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()    
    return FormatURLNode(bits[1])

# this can be removed/optimized
def formaturl(parser, token):
    return do_formaturl(parser, token)

class FormatURLNode(Node):    
    def __init__(self, var1):
        self.var1 = Variable(var1)

    def __repr__(self):
        return "<FormatTimeNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        cache_key = '%s_quiptext%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,)
        kwip = cache.get(cache_key)
        if kwip is None:
            quip = get_object_or_404(Quip, id=val1)
            text = quip.original.strip()
            match = re.match(regex,text)
            if match:
                url = match.group(1)
                replacement = '<a target="blank" href='+url+'>'+url+'</a>'
                kwip = text.replace(url,replacement)
            else:
                kwip = quip.original
            cache.set(cache_key,kwip,86400)
        return kwip

register.tag('formaturl',do_formaturl)
