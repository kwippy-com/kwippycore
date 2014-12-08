from django.db import models
from django.contrib.auth.models import *

#syntax for email/IM settings would be in order comment,follower,private_message,buzz

class NotificationSetting(models.Model):    
    user = models.ForeignKey(User, related_name="user")
    email = models.CharField(max_length=100,default='1,1,1,1,0,1,1,1', blank=False, null=False)
    im = models.CharField(max_length=100,default='1,1,1,1,1,1,1,1', blank=False, null=False)    
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self) :
        return '%s %s' % (self.user, self.email)

    class Meta:
	app_label="kwippy"	

