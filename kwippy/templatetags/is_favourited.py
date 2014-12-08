from kwippyproject.kwippy.models.quip import Quip
from kwippyproject.kwippy.models.favourite import Favourite
from django.contrib.auth.models import User
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.conf import settings
from django.core.cache import cache
import pdb

register = template.Library()

def do_show_is_favourite(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return IsFavouriteNode(bits[1], bits[2])

def show_is_favourite(parser, token):
    return do_show_is_favourite(parser, token)

def is_favorite(quip,user):
    following = Favourite.objects.filter(quip=quip,user=user)
    if following:
        return True
    return False

class IsFavouriteNode(Node):
    def __init__(self, var1, var2):
        self.var1 = Variable(var1)
	self.var2 = Variable(var2)
        
    def __repr__(self):
        return "<IsFavouriteNode>"
    
    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        try:
            val2 = self.var2.resolve(context)
        except VariableDoesNotExist:
            val2 = None
        
        cache_key = '%s_user%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,)
        user = cache.get(cache_key)
        if user is None:
            user = get_object_or_404(User, id=val1)
            cache.set(cache_key,user,86400)
        
        cache_key = '%s_quip%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val2,)
        quip = cache.get(cache_key)
        if quip is None:
            quip = get_object_or_404(Quip, id=val2)	
            cache.set(cache_key,quip,86400)
        
        cache_key = '%s_fav%d-%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,val2,)
        following = cache.get(cache_key)
        if following is None:
            following = is_favorite(quip,user)
            cache.set(cache_key,following,86400)
            
	if following:
          html =  "<a align=\"left\" onclick=\"favorite_unfavorite("+str(quip.id)+")\" href=\"javascript:void(0);\"  id=\"unfavorite_"+str(quip.id)+"\"><img id=\"unfav_image_"+str(quip.id)+"\" class=\"go_icon\" title=\"remove this kwip from bookmarks\" src=\"/images/icons/bookmark_add.gif\" /></a> |"
          return html
	else:
          html =  "<a align=\"left\" onclick=\"favorite_unfavorite("+str(quip.id)+")\" href=\"javascript:void(0);\" id=\"favorite_"+str(quip.id)+"\"><img id=\"fav_image_"+str(quip.id)+"\" class=\"go_icon\" title=\"bookmark this kwip\" src=\"/images/icons/bookmark_remove.gif\" /></a> |"
          return html

        
register.tag('show_is_favourite',do_show_is_favourite)
