from django.contrib.auth.models import *
from kwippyproject.kwippy.models.user_profile import User_Profile
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.conf import settings
from django.core.cache import cache
from django.utils.html import strip_tags
import pdb

register = template.Library()

def do_say_hi_people(parser, token):    
    bits = list(token.split_contents())
    nodelist = NodeList()
    return SayHiPeopleNode(bits[1])

def say_hi_people(parser, token):
    return do_say_hi_people(parser, token)
    
class SayHiPeopleNode(Node):
    def __init__(self, var1):
        self.var1 = Variable(var1)
                
    def __repr__(self):
        return "<SayHiPeople>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        
        cache_key = '%s_user%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,)
        user = cache.get(cache_key)
        if user is None:
            user = get_object_or_404(User, id=val1)
            cache.set(cache_key,user,86400)
        
        cache_key = '%s_profilequery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,)
        user_profile = cache.get(cache_key)
        if user_profile is None:
            user_profile = get_object_or_404(User_Profile, user=user)
            cache.set(cache_key, user_profile, 86400)
	def ret_gender(gender):
            if gender==1:
                return "male"
            return "female"
        html = "say hi to our new member <b>%s</b> :)." % (user.username,)
        if user_profile.age and user_profile.gender and user_profile.location_city:
            html+= "<br>a lil about <b>%s</b>. (<b>%d | %s | %s</b>)" % (user.username,user_profile.age,ret_gender(user_profile.gender),user_profile.location_city,)
        #    if user_profile.about_me:
        #        html+= "<br>\"%s\"" % (strip_tags(user_profile.about_me),)
        #    return html
        #if user_profile.about_me:
        #    html+= "<br>a lil about <b>%s</b>. \"%s\"" % (strip_tags(user_profile.about_me),)
            
        return html
        
register.tag('say_hi_people',do_say_hi_people)
