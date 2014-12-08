from django.db import models
from django.contrib.auth.models import *
from kwippyproject.kwippy.models.private_message import Private_Message

# List Filter
class Sent_Filter(models.Model):    
    sender_user = models.ForeignKey(User)
    pm = models.ForeignKey(Private_Message)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self) :	
        return '%s %s' % (self.sender, self.message)
  
    class Meta:
	app_label="kwippy"	
	 