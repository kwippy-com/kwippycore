from django.contrib.auth.models import *
from kwippyproject.kwippy.models.user_profile import User_Profile
from django import template
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.core.cache import cache
import pdb

register = template.Library()

def do_show_followee_pic(parser, token):    
    bits = list(token.split_contents())
    nodelist = NodeList()    
    return ShowFolloweePicNode(bits[1])

def show_follower_pic(parser, token):
    return do_show_followee_pic(parser, token)
    
class ShowFolloweePicNode(Node):
    def __init__(self, var1):
        self.var1 = Variable(var1)        
        
    def __repr__(self):
        return "<ShowFolloweePicNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        cache_key = '%s_profilequery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,)
        user_profile = cache.get(cache_key)
	s3_path = "http://s3.amazonaws.com/"+settings.BUCKET_NAME+'/'
        if user_profile is None:
            user = get_object_or_404(User, id=val1)
            user_profile = get_object_or_404(User_Profile, user=user)
            cache.set(cache_key, user_profile, 3600)
            
        if user_profile.media_processed==2:
		# return path for pic for follower and followee sections                 
                image_path = s3_path + str(val1) +"."+ str(user_profile.picture_ver) + '.following'
                #image_path = s3_path + str(5) + '.thumbnail2' 
        else:
                gender = user_profile.gender
                if gender:
                    if gender==1:
                        image_path = s3_path+"dude.0.following"
                    elif gender==2:
                        image_path = s3_path+"duddette.0.following"
                else:#unisex image
                    image_path = s3_path+"unisex.0.following"                 
        return image_path
        
register.tag('show_followee_pic',do_show_followee_pic)
