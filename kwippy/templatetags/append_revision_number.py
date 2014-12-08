from django.contrib.auth.models import *
from kwippyproject.kwippy.models.user_profile import User_Profile
from django import template
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable

register = template.Library()

def do_append_revision_number(parser, token):    
    bits = list(token.split_contents())
    nodelist = NodeList()    
    return AppendRevisionNumberNode(bits[1])

def append_revision_number(parser, token):
    return do_append_revision_number(parser, token)
    
class AppendRevisionNumberNode(Node):
    def __init__(self, var1):
        self.var1 = Variable(var1)
                
    def __repr__(self):
        return "<AppendRevisionNumberNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
		
        if settings.REVISION_NUMBER==0:
		    return val1
        else:
		    return val1+"."+str(settings.REVISION_NUMBER)
        
register.tag('append_revision_number',do_append_revision_number)
