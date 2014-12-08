from django.db import models
from django.contrib.auth.models import *
from kwippyproject.kwippy.models.account import Account

# PrivateMessage profile
class Private_Message(models.Model):    
    sender = models.ForeignKey(User,related_name="sender")
    receiver = models.ForeignKey(User,related_name="receiver") 
    message = models.TextField()
    account = models.ForeignKey(Account)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self) :	
        return '%s %s %s' % (self.sender, self.receiver, self.message)
  
    class Meta:
	app_label="kwippy"	
	 