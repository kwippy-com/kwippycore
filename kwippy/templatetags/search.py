from kwippyproject.kwippy.models.quip import Quip
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
import pdb, re, string
from kwippy.views.main import ireplace
from django.conf import settings

register = template.Library()

def do_formatquery(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()    
    return FormatQueryNode(bits[1],bits[2])

def formatquery(parser, token):
    return do_formatquery(parser, token)

class FormatQueryNode(Node):    
    def __init__(self, var1, var2):
        self.var1 = Variable(var1)
        self.var2 = Variable(var2)
    def __repr__(self):
        return "<FormatQueryNode>"

    def render(self, context):        
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        try:
            val2 = self.var2.resolve(context)
        except VariableDoesNotExist:
            val2 = None                    
        query = val1
        text = val2
        replacement = '<span class="highlighter">'+query+'</span>'
        data_object = ireplace(text,query,replacement)
        return data_object
        
register.tag('formatquery',do_formatquery)
