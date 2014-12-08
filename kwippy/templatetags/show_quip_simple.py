from kwippyproject.kwippy.models.quip import Quip
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.core.cache import cache
from django.conf import settings
from django.utils.html import *
import pdb

register = template.Library()

entries = [(":)",":-)"),(":-{}",":-*"),(":-$",":$",":-|"),("*KISSING*",),(":(",":-("),(":-[",":-<"), ("=-O",":-O"),("]:->",),(";-)",";)"),("O:-)","o:-)","O-)","o-)"),("8-)","8)"),("@}->--",), (":P",":-P"),(":X",":-X"),("[:-}",),("@=","=@"),("*JOKINGLY*",),(":-\\",':-/'),("*TIRED*",), ("*THUMBS UP*",),(":'-(",":'("),(":-@",">:O",">:o"),(":-!",":*)"),("*DRINK*",),("*KISSED*",), (":-D",":D"),("*STOP*",),("*IN LOVE*",)]

def do_showquipsimple(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return ShowQuipSimpleNode(bits[1])

def displayprovider(parser, token):
    return do_displayprovider(parser, token)

class ShowQuipSimpleNode(Node):
    def __init__(self, var1):
        self.var1 = Variable(var1)
    def __repr__(self):
        return "<ShowQuipSimpleNode>"
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
        quip = get_object_or_404(Quip, id=val1)
        ret_str = ''
        if not quip.formated:
            quip.formated=quip.original
        ret_str = quip.formated
        ret_str = urlize(escape(ret_str)).replace('\n', '<br /> ')
        count = 0
        for entry in entries:
            count = count + 1
            for e in entry:
                ret_str = ret_str.replace(e,"<img src='/images/icons/smallSmiley"+str(count)+".gif'/>")
        return ret_str

register.tag('showquipsimple',do_showquipsimple)
