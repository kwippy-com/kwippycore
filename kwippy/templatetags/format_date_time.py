from kwippyproject.kwippy.models.quip import Quip
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.core.cache import cache
from django.conf import settings

register = template.Library()

def do_formattime(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return FormatTimeNode(bits[1])

def formattime(parser, token):
    return do_formattime(parser, token)

class FormatTimeNode(Node):
    def __init__(self, var1):
        self.var1 = Variable(var1)
        
    def __repr__(self):
        return "<FormatTimeNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        quip = get_object_or_404(Quip, id=val1)
	link = '/'+quip.user.username+'/kwip/'+str(quip.id)+'/'
        return link
        
register.tag('formattime',do_formattime)
