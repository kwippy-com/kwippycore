from django.db import models
from django.contrib.auth.models import *
from kwippyproject.kwippy.models.account import *
from kwippyproject.kwippy.models.user_profile import *
from djangosphinx import SphinxSearch
from django.contrib.comments.models import Comment
from django.shortcuts import render_to_response, get_object_or_404

class AutoDateTimeField(models.DateTimeField):	
        def pre_save(self, model_instance, add):
		return datetime.datetime.now()	 

def everyone_count():
   return 1000 

def user_kwips_count(user_id):
   up = get_object_or_404(User_Profile,user__id=user_id)
   return up.quip_total

def user_repeat_kwips_count(user_id):
    up = get_object_or_404(User_Profile,user__id=user_id)
    return up.quip_repeat_total

def user_network_count(user_id):
   return 1000

class QuipManager(models.Manager):
    def user_kwips_repeat(self,user_id,filter_col,page,paginate_by):
        condition = "kwippy_quip.user_id=%d" % (user_id,)
        start = page*paginate_by
        order = '-kwippy_quip.%s' % (filter_col,)
        query_set = self.get_query_set().extra(tables=[],where=[condition]).order_by(order)[start:start+paginate_by]
        query_set.count = user_repeat_kwips_count(user_id)
        return query_set
    def user_kwips(self,user_id,filter_col,page,paginate_by):
        condition = "kwippy_quip.is_filtered=1 and kwippy_quip.user_id=%d" % (user_id,)
        order = '-kwippy_quip.id'
        start = page*paginate_by
        query_set =  self.get_query_set().extra(tables=[],where=[condition]).order_by(order)[start:start+paginate_by]
        query_set.count = user_kwips_count(user_id)
        return query_set        
    def user_network_kwips(self,user_id,filter_col,page,paginate_by):
        condition = "kwippy_quip.is_filtered=1 and kwippy_quip.user_id=kwippy_follower.followee_id and kwippy_follower.follower_id=%s" % (user_id,)
        order = '-kwippy_quip.%s' % (filter_col,)
        start = page*paginate_by
        query_set =  self.get_query_set().extra(tables=['kwippy_follower'],where=[condition]).order_by(order)[start:start+paginate_by]
        query_set.count = user_network_count(user_id)
        return query_set
    def user_network_kwips_geo(self,user_id,location,page,paginate_by):
        condition = "repeat_id in (id,0) and user_id in (select kwippy_fireeagle.user_id from kwippy_fireeagle where kwippy_fireeagle.location like '%s' and kwippy_fireeagle.integrated=1) and (user_id in (select followee_id from kwippy_follower where follower_id=%s) or user_id=%s)" % (location,user_id,user_id,)
        order = '-kwippy_quip.id'
        start = page*paginate_by
        query_set = self.get_query_set().extra(tables=[],where=[condition]).order_by(order)[start:start+paginate_by]
        query_set.count = user_network_count(user_id)
        return query_set
    def everyone(self,filter_col,page,paginate_by):
        condition = """kwippy_quip.is_filtered=1""" # and  user_id is not null and user_id > 0"""
        start = page*paginate_by
        order = '-kwippy_quip.%s' % (filter_col,)
        query_set = self.get_query_set().extra(tables=[],where=[condition]).order_by(order)[start:start+paginate_by]
        query_set.count = everyone_count()
        return query_set
    def everyone_geo(self,location,page,paginate_by):
        condition = "kwippy_quip.is_filtered=1 and user_id in (select user_id from kwippy_fireeagle where kwippy_fireeagle.location like '%s' and kwippy_fireeagle.integrated=1)" % (location,)
        order = '-kwippy_quip.id'
        start = page*paginate_by
        query_set = self.get_query_set().extra(tables=[],where=[condition]).order_by(order)[start:start+paginate_by]
        query_set.count = everyone_count()
        return query_set
        

# Quip profile
class Quip(models.Model):
        objects = QuipManager()
        user = models.ForeignKey(User,null = True, default=None)
	original = models.TextField()
	formated = models.TextField(blank=True, null=True, default=None)    
	account = models.ForeignKey(Account)
	primitive_state = models.CharField(max_length=40,blank=True, null=True, default=None)
        type = models.IntegerField(default=0)
	is_filtered = models.IntegerField(default=0)
        repeat = models.ForeignKey("Quip", default=0)
        last_comment_at = models.DateTimeField(blank=True,null=True)
        comment_count = models.IntegerField(default=0)
        last_comment = models.ForeignKey(Comment, blank=True, null=True, related_name="last_comment")
	created_at = models.DateTimeField(auto_now_add=True)
        search = SphinxSearch(index="main1")
        	
	def __unicode__(self) :		
		return '%s %s %s %d' % (self.original, self.formated, self.primitive_state, self.is_filtered)	
        
	class Meta:	
		app_label="kwippy"	

	def quips_on_same_time(self):
		"""
		Returns all the kwips within the exact the same second by same user
		coz if the users are different the time based url's will be different anyways
		since they include the username. ex http://127.0.0.1:1000/mayank/kwips/2008/jan/26/204703/
		and http://127.0.0.1:1000/dipankar/kwips/2008/jan/26/204703/ same datetime but different urls
		"""
		quip_time = self.created_at
		user = self.account.user
		accounts = Account.objects.filter(user=user,status=1)
		quips = Quip.objects.filter(created_at=quip_time,account__in=accounts)
		if len(quips)>1:
			dict = {}
			id = 1
			for q in quips:
				dict[q.id]= id
				id = id + 1
			return dict
		else:
			return quips

        def get_absolute_url(self):
                if self.user:
		    link = '/%s/kwip/%d/' % (self.user.username,self.id,)
                    return link
		return '/'
                
	def quips_on_same_time_serial(self,serial):
		quip_time = self.created_at
		user = self.account.user
		accounts = Account.objects.filter(user=user,status=1)
		quips = Quip.objects.filter(created_at=quip_time,account__in=accounts)
		dict = {}
		id = 1
		for q in quips:
			if id==serial:
				return Quip.objects.filter(id=q.id)
			id = id + 1
		return 
