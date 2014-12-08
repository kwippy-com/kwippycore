from django.contrib.auth.models import *
from django.contrib.syndication.feeds import Feed
from django.contrib.syndication.feeds import FeedDoesNotExist
from kwippy.models.quip import Quip
from django.contrib.comments.models import Comment
from kwippy.views.views import queryset_to_csv
from django.conf import settings
import datetime

class PublicTimelineFeed(Feed):
    title = "Kwippy public timeline feed"
    link = "http://kwippy.com"
    description = "Public timeline from kwippers all around the world."
    
    def items(self):
        quips = Quip.objects.filter(is_filtered=1).order_by("-id")[0:20]
        return quips

    def item_pubdate(self,item):
        """
        Returns the pubdate for every item in the feed.
        """
        return item.created_at

    def item_author_name(self,item):
        """
        Takes the object returned by get_object() and returns the feed's
        author's name as a normal Python string.
        """
        return item.user.username


class ActivePublicTimelineFeed(Feed):
    title = "Kwippy public timeline feed"
    link = "http://kwippy.com"
    description = "Public timeline from kwippers all around the world by activity."
    
    def items(self):
        quips = Quip.objects.everyone("last_comment_at",0,20)
        return quips

    def item_pubdate(self,item):
        """
        Returns the pubdate for every item in the feed.
        """
        return item.created_at

    def item_author_name(self,item):
        """
        Takes the object returned by get_object() and returns the feed's
        author's name as a normal Python string.
        """
        return item.user.username



class FriendsTimelineFeed(Feed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return User.objects.get(username__exact=bits[0])

    def title(self, obj):
        return "Kwippy feed for %s and his friends" % obj.username
    
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return "http://kwippy.com/%s/kwips" % obj.username

    def description(self, obj):
        return "These are the recent kwips by %s and his friends" % obj.username

    def items(self, obj):
        quips = Quip.objects.user_network_kwips(obj.id,"id",0,20)
        return quips

    def item_pubdate(self,item):
        """
        Returns the pubdate for every item in the feed.
        """
        return item.created_at

    def item_author_name(self,item):
        """
        Takes the object returned by get_object() and returns the feed's
        author's name as a normal Python string.
        """
        return item.user.username    
    
class ActiveFriendsTimelineFeed(Feed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return User.objects.get(username__exact=bits[0])

    def title(self, obj):
        return "Kwippy feed for %s and his friends by activity" % obj.username
    
    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return "http://kwippy.com/%s/kwips" % obj.username

    def description(self, obj):
        return "These are the active kwips by %s and his friends" % obj.username

    def items(self, obj):
        quips = Quip.objects.user_network_kwips(obj.id,"last_comment_at",0,20)
        return quips

    def item_pubdate(self,item):
        """
        Returns the pubdate for every item in the feed.
        """
        return item.created_at

    def item_author_name(self,item):
        """
        Takes the object returned by get_object() and returns the feed's
        author's name as a normal Python string.
        """
        return item.user.username    
    


class UserTimelineFeed(Feed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return User.objects.get(username__exact=bits[0])

    def title(self, obj):
        return "Kwippy feed for %s" % obj.username

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return "http://kwippy.com/%s" % obj.username

    def description(self, obj):
        return "These are the recent kwips by %s" % obj.username

    def items(self, obj):
        quips = Quip.objects.user_kwips(obj.id,"id",0,20)
        return quips

    def item_pubdate(self,item):
        """
        Returns the pubdate for every item in the feed.
        """
        return item.created_at

    def item_author_name(self,item):
        """
        Takes the object returned by get_object() and returns the feed's
        author's name as a normal Python string.
        """
        return item.user.username
    


class FavoriteFeed(Feed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return User.objects.get(username__exact=bits[0])

    def title(self, obj):
        return "Kwippy favorite feed for %s" % obj.username

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return "http://kwippy.com/%s" % obj.username

    def description(self, obj):
        return "These are the recent favorite kwips by %s" % obj.username

    def items(self, obj):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("select id from kwippy_quip where id in (select quip_id from kwippy_favourite where user_id=%s) order by created_at desc limit 20 ", (obj.id,))
        quip_ids = [item[0] for item in cursor.fetchall()]
        quips = Quip.objects.filter(id__in=quip_ids).order_by('-created_at')
	cursor.close()
        return quips

    def item_pubdate(self,item):
        """
        Returns the pubdate for every item in the feed.
        """
        return item.created_at

    def item_author_name(self,item):
        """
        Takes the object returned by get_object() and returns the feed's
        author's name as a normal Python string.
        """
        return item.user.username
    

class RepliesFeed(Feed):
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Quip.objects.get(id__exact=bits[0])
	
    def title(self, obj):
        return "Kwippy comments feed for %s" % obj.formated

    def link(self, obj):
        if not obj:
            raise FeedDoesNotExist
        return "http://kwippy.com/%s" % obj

    def description(self, obj):
        return "These are the recent comments on kwip %s" % obj.formated

    def items(self, obj):
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("select id from django_comments where object_pk=%s and content_type_id=19 limit 20 ", (obj.id,))
        comment_ids = [item[0] for item in cursor.fetchall()]
        comments = Comment.objects.filter(id__in=comment_ids).order_by('-submit_date')
	cursor.close()
        return comments

    def item_pubdate(self,item):
        """
        Returns the pubdate for every item in the feed.
        """
        return item.submit_date

    def item_author_name(self,item):
        """
        Takes the object returned by get_object() and returns the feed's
        author's name as a normal Python string.
        """
        return item.user.username


class FriendsFeed(Feed):
    title = "Chicagocrime.org site news"
    link = "/sitenews/"
    description = "Updates on changes and additions to chicagocrime.org."
    
    def item_link(self):
        return "hi"
    
    def items(self):
        print "hello"
        return Quip.objects.order_by('-created_at')[:5]

class FollowersFeed(Feed):
    title = "Chicagocrime.org site news"
    link = "/sitenews/"
    description = "Updates on changes and additions to chicagocrime.org."
    
    def item_link(self):
        return "hi"
    
    def items(self):
        print "hello"
        return Quip.objects.order_by('-created_at')[:5]
