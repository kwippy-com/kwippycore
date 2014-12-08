from django.contrib.comments.models import Comment
from kwippyproject.kwippy.models.favourite_comment import Favourite_Comment
from django.contrib.auth.models import User
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.conf import settings
from django.core.cache import cache
import pdb

register = template.Library()

def do_show_is_favourite_comment(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return IsFavouriteCommentNode(bits[1], bits[2])

def show_is_favourite_comment(parser, token):
    return do_show_is_favourite_comment(parser, token)

def is_favorite_comment(comment,user):
    following = Favourite_Comment.objects.filter(comment=comment,user=user)
    if following:
        return True
    return False

class IsFavouriteCommentNode(Node):
    def __init__(self, var1, var2):
        self.var1 = Variable(var1)
	self.var2 = Variable(var2)
        
    def __repr__(self):
        return "<IsFavouriteCommentNode>"
    
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
        
        cache_key = '%s_comment%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val2,)
        comment = cache.get(cache_key)
        if comment is None:
            comment = get_object_or_404(Comment, id=val2)	
            cache.set(cache_key,comment,86400)
        
        cache_key = '%s_fav_com%d-%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,val1,val2,)
        following = cache.get(cache_key)
        if following is None:
            following = is_favorite_comment(comment,user)
            cache.set(cache_key,following,86400)
            
	if following:
          html =  "<a align=\"left\" onclick=\"favorite_unfavorite_comment("+str(comment.id)+")\" href=\"javascript:void(0);\"  id=\"unfavorite_"+str(comment.id)+"\"><img id=\"unfav_image_"+str(comment.id)+"\" class=\"go_icon\" title=\"unfavorite this comment\" src=\"/images/icons/unfavorite.gif\" /></a> |"
          return html
	else:
          html =  "<a align=\"left\" onclick=\"favorite_unfavorite_comment("+str(comment.id)+")\" href=\"javascript:void(0);\" id=\"favorite_"+str(comment.id)+"\"><img id=\"fav_image_"+str(comment.id)+"\" class=\"go_icon\" title=\"favorite this comment\" src=\"/images/icons/favorite.gif\" /></a> |"
          return html

        
register.tag('show_is_favourite_comment',do_show_is_favourite_comment)
