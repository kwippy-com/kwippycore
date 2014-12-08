from django.contrib.auth.models import *
from kwippyproject.kwippy.models.user_profile import User_Profile
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.conf import settings
from django.core.cache import cache
import pdb
import datetime

register = template.Library()

def do_show_big_pic(parser, token):    
    bits = list(token.split_contents())
    nodelist = NodeList()    
    return ShowBigPicNode(bits[1])

def show_big_pic(parser, token):
    return do_show_big_pic(parser, token)
    
class ShowBigPicNode(Node):
    def __init__(self, var1):
        self.var1 = Variable(var1)
                
    def __repr__(self):
        return "<ShowBigPicNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        cache_key = '%s_profilequery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,)
        user_profile = cache.get(cache_key)
        user = get_object_or_404(User, id=val1)
        
	s3_path = "http://s3.amazonaws.com/"+settings.BUCKET_NAME+'/' 
        if user_profile is None:
            user_profile = get_object_or_404(User_Profile, user=user)
            cache.set(cache_key, user_profile, 86400)
            
        # From 18th August
        if user_profile.media_processed == 2 and user.date_joined>datetime.datetime(2008, 8, 19):
                # return path for pic for main/kwips page
                image_path = s3_path + str(val1) +"."+ str(user_profile.picture_ver) + '.big'
        elif user_profile.media_processed == 2:
                image_path = s3_path + str(val1) +"."+ str(user_profile.picture_ver) + '.main'
	else:
		gender = user_profile.gender
                if gender:
                    if gender==1:
                        image_path = s3_path+"dude.0.main"
                    elif gender==2:
                        image_path = s3_path+"duddette.0.main"
                else:#unisex image
                    image_path = s3_path+"unisex.0.main"
        return image_path

register.tag('show_big_pic',do_show_big_pic)
