from django.db import models
from django.contrib.auth.models import *
from kwippyproject.kwippy.models.invite import Invite

# Invite profile
class Invite_Limit(models.Model):
    invite = models.ForeignKey(Invite)
    maxcount = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self) :
	return '%d' % (self.count)
    
    class Meta:	
	app_label="kwippy"	

