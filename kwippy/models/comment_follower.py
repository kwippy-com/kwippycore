from django.db import models
from django.contrib.auth.models import *
from kwippyproject.kwippy.models.quip import *

# Follower profile
class Comment_Follower(models.Model):    
    user = models.ForeignKey(User,related_name="comment_follower")
    quip = models.ForeignKey(Quip,related_name="followed_quip") 
    is_active = models.IntegerField(blank=False, null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self) :	
        return '%s %s' % (self.user, self.quip)
  
    class Meta:
	app_label="kwippy"	
