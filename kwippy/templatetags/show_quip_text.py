from kwippyproject.kwippy.models.user_profile import User_Profile
from kwippyproject.kwippy.models.quip import Quip
from django import template
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.core.cache import cache
import pdb

register = template.Library()

def do_show_quip_text(parser, token):    
    bits = list(token.split_contents())
    nodelist = NodeList()    
    return ShowQuipTextNode(bits[1])

def show_quip_text(parser, token):
    return do_show_quip_text(parser, token)
    
class ShowQuipTextNode(Node):
    def __init__(self, var1):
        self.var1 = Variable(var1)
        
    def __repr__(self):
        return "<ShowQuipTextNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        quip = Quip.objects.filter(id=val1)#get_object_or_404(Quip, id=val1)
        if quip:
            return quip[0].user.username+"'s kwip *"+ quip[0].formated[:50] + "...*"
        else:
            return ""
        
register.tag('show_quip_text',do_show_quip_text)
