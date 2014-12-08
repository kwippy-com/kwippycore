from django.db import models
from django.contrib.auth.models import *
from kwippyproject.kwippy.models.account import Account

BUZZ_TYPES = ((1,'Quip'), (2,'Profile-Pic'))

# Buzz profile
class Buzz(models.Model):    
    sender = models.ForeignKey(User,related_name="buzz_sender")
    receiver = models.ForeignKey(User,related_name="buzz_receiver") 
    message = models.CharField(max_length=500)
    buzz_type = models.IntegerField(choices=BUZZ_TYPES, max_length=2, default=0) 
    account = models.ForeignKey(Account)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self) :	
        return '%s %s %s %s' % (self.sender, self.receiver, self.message, self.account)
  
    class Meta:
	app_label="kwippy"	

