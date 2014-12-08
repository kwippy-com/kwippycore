from kwippyproject.kwippy.models.quip import Quip
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.core.cache import cache
from django.conf import settings
from django.utils.html import *
import pdb

register = template.Library()

def do_sniptomore1(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return SnipToMore1Node(bits[1])

def displayprovider(parser, token):
    return do_displayprovider(parser, token)

class SnipToMore1Node(Node):
    def __init__(self, var1):
        self.var1 = Variable(var1)
    def __repr__(self):
        return "<SnipToMore1Node>"
    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        cache_key = '%s_quiplink%d' %(settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1)
        link = cache.get(cache_key)
        if link is None:
            quip = get_object_or_404(Quip, id=val1)
            kwips = quip.quips_on_same_time()
            user = quip.account.user.username
            timestamp = quip.created_at.strftime("%Y/%b/%d/%H%M%S")
            link = user+'/kwips/'+timestamp.lower()
            if len(kwips)>1:
                link = link + '/' + str(kwips[quip.id])
            cache.set(cache_key, link, 86400)
        cache_key = '%s_quip_short%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,)
        ret_str = cache.get(cache_key)
        if ret_str is None:
            quip = get_object_or_404(Quip, id=val1)
            ret_str = ''
            append = 0
            if not quip.formated:
                quip.formated=quip.original
            quip.formated=strip_tags(quip.formated)
            if(quip.formated.count('\n')>settings.MAX_LINE_BREAKS):
                count = 0
                for ch in quip.formated:
                    if ch=='\n':
                        count=count+1
                    if count>settings.MAX_LINE_BREAKS:
                        break
                    ret_str=ret_str+ch
                append = 1
            elif(len(quip.formated)>settings.MAX_STR_LENGTH):
                ret_str = quip.formated[:settings.MAX_STR_LENGTH]
                ret_str = ret_str[:ret_str.rfind(' ')]
                append = 1
            else:
                ret_str = quip.formated
            if append==1:
                ret_str = ret_str + ' ... <a href="'+settings.SITE+"/"+link+'">more</a>'
            cache.set(cache_key,ret_str,86400)
        return ret_str

register.tag('sniptomore1',do_sniptomore1)