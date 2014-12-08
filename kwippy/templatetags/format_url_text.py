from kwippyproject.kwippy.models.quip import Quip
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.conf import settings
import pdb, re

register = template.Library()

regex = re.compile('^.*(https?:\/\/[^\ \s]*).*$')


def do_formaturl_text(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()    
    return FormatURLTextNode(bits[1])

# this can be removed/optimized
def formaturltext(parser, token):
    return do_formaturl_text(parser, token)

class FormatURLTextNode(Node):    
    def __init__(self, var1):
        self.var1 = Variable(var1)
        
    def __repr__(self):
        return "<FormatTimeNode>"

    def render(self, context):        
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        if val1:
            text = val1.strip()
            match = re.match(regex,text)
            if match:                
                url = match.group(1)
                replacement = '<a target="blank" href='+url+'>'+url+'</a>'
                text = text.replace(url,replacement)
            else:
                text  = text           
            return  text 
        
register.tag('formaturltext',do_formaturl_text)
