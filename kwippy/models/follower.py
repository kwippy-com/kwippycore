from django.db import models
from django.contrib.auth.models import *

# Follower profile
class Follower(models.Model):    
    follower = models.ForeignKey(User,related_name="follower")
    followee = models.ForeignKey(User,related_name="followee")
    im_notification = models.BooleanField(default=0, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self) :	
        return '%s %s' % (self.follower, self.followee)
  
    class Meta:
	app_label="kwippy"	

