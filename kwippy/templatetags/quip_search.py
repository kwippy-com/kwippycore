from kwippyproject.kwippy.models.quip import Quip
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
import pdb, re, string
from kwippy.views.main import ireplace
from django.conf import settings

register = template.Library()

def do_formatquipquery(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()    
    return FormatQuipQueryNode(bits[1],bits[2])

def formatquipquery(parser, token):
    return do_formatquipquery(parser, token)

class FormatQuipQueryNode(Node):    
    def __init__(self, var1, var2):
        self.var1 = Variable(var1)
        self.var2 = Variable(var2)
    def __repr__(self):
        return "<FormatQuipQueryNode>"

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
        location = string.find(text.upper(),query.upper())
        if location>40:
            cropped_text = text[location-40:location+40]
            text = "..."+cropped_text+"..."
        else:
            cropped_text = text[:location+40]
            text = cropped_text+"..."
        replacement = '<span class="highlighter">'+query+'</span>'
        data_object = ireplace(text,query,replacement)
        return data_object
        
register.tag('formatquipquery',do_formatquipquery)
