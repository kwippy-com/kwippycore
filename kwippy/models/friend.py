from django.db import models
from django.contrib.auth.models import *

FRIENDSHIP_STATUS_CHOICES = ((-1,'Declined'), (0,'Pending'), (1,'Accepted'))

# Friend profile
class Friend(models.Model):    
    sender = models.ForeignKey(User,related_name="friendship_sender")
    receiver = models.ForeignKey(User,related_name="friendship_receiver")
    status = models.IntegerField(choices=FRIENDSHIP_STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self) :	
        return '%s %s' % (self.sender, self.receiver)
  
    class Meta:
	app_label="kwippy"	

