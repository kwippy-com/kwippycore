from django.contrib.auth.models import *
from kwippyproject.kwippy.models.user_profile import User_Profile
from django import template
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.core.cache import cache
import pdb

register = template.Library()

def do_show_follower_pic(parser, token):    
    bits = list(token.split_contents())
    nodelist = NodeList()    
    return ShowFollowerPicNode(bits[1])

def show_follower_pic(parser, token):
    return do_show_follower_pic(parser, token)
    
class ShowFollowerPicNode(Node):
    def __init__(self, var1):
        self.var1 = Variable(var1)        
        
    def __repr__(self):
        return "<ShowFollowerPicNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        cache_key = '%s_profilequery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,)
        user_profile = cache.get(cache_key)
        if user_profile is None:
            user = User.objects.get(id=val1)
            user_profile = get_object_or_404(User_Profile, user=user)
            cache.set(cache_key, user_profile, 86400)
            
        s3_path = "http://s3.amazonaws.com/"+settings.BUCKET_NAME+'/'
        if user_profile:
            if user_profile.media_processed==2:                
                # return path for pic for follower and followee sections                    
                image_path = s3_path + str(val1) +"."+ str(user_profile.picture_ver) + '.follower'                
            else:
                gender = user_profile.gender
                if gender:
                    if gender==1:
                        image_path = s3_path+"dude.0.follower"
                    elif gender==2:
                        image_path = s3_path+"duddette.0.follower"
                else:#unisex image
                    image_path = s3_path+"unisex.0.follower"                
            return image_path
        
register.tag('show_follower_pic',do_show_follower_pic)
