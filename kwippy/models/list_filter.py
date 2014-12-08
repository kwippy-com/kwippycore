from django.db import models
from django.contrib.auth.models import *
from kwippyproject.kwippy.models.private_message import Private_Message

# List Filter
class List_Filter(models.Model):    
    receiver_user = models.ForeignKey(User)
    pm = models.ForeignKey(Private_Message)
    status = models.BooleanField(default=0, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self) : 
        return '%s %s' % (self.receiver_user, self.pm)
  
    class Meta:
	app_label="kwippy"	

