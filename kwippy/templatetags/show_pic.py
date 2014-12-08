from django.contrib.auth.models import *
from kwippyproject.kwippy.models.user_profile import User_Profile
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.core.cache import cache
from django.conf import settings
import pdb

register = template.Library()

def do_show_thumbnail(parser, token):    
    bits = list(token.split_contents())
    nodelist = NodeList()    
    return ShowThumbnailNode(bits[1],bits[2])

def show_thumbnail(parser, token):
    return do_show_thumbnail(parser, token)
    
class ShowThumbnailNode(Node):
    def __init__(self, var1, var2):
        self.var1 = Variable(var1)
        self.var2 = Variable(var2)
        
    def __repr__(self):
        return "<ShowThumbnailNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        try:
            val2 = self.var2.resolve(context)            
        except VariableDoesNotExist:
            val2 = None
        s3_path = "http://s3.amazonaws.com/kwippy-test/"            
        if val2 =='main':  # return path for pic for main/kwips page              
                image_path = s3_path + str(val1) + '.thumbnail1'
        else:
		# return path for pic for follower and followee sections
                image_path = s3_path + str(val1) + '.thumbnail2'                               
        return image_path
        
register.tag('show_thumbnail',do_show_thumbnail)
