from django.db import models
from django.contrib.auth.models import *
from kwippyproject.kwippy.models.quip import *

# Follower profile
class Anon_Comment_Follower(models.Model):    
    user = models.ForeignKey(User,related_name="anon_comment_follower")
    quip = models.ForeignKey(Quip,related_name="anon_followed_quip") 
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self) :	
        return '%s %s' % (self.user, self.quip)
  
    class Meta:
	app_label="kwippy"	

