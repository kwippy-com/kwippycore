from kwippyproject.kwippy.models.quip import Quip
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.conf import settings
from django.core.cache import cache
import datetime
import pdb

register = template.Library()

def do_comment_active(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return IsCommentActive(bits[1])

def show_comment_active(parser, token):
    return do_comment_active(parser, token)

class IsCommentActive(Node):
    def __init__(self, var1):
        self.var1 = Variable(var1)
        
    def __repr__(self):
        return "<IsCommentActive>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        
        cache_key = '%s_quip%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,)
        quip = cache.get(cache_key)
        if quip is None:
            quip = Quip.objects.get(id=val1)
            cache.set(cache_key,quip,86400)
        html = ""
        if quip.last_comment_at:
            if (quip.last_comment_at-datetime.datetime.now())<datetime.timedelta(1):
                html = '''|<img class="link_icon" title="active in last 24 hours" src="/images/icons/talking.gif">'''
	return html

register.tag('comment_active',do_comment_active)
