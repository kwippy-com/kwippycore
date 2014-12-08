from django.db import models
from django.contrib.auth.models import User
from kwippyproject.kwippy.models.quip import Quip

# Invite profile
class Anon_Conversation_Invite(models.Model):
    quip = models.ForeignKey(Quip)
    sender = models.ForeignKey(User)
    receiver = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self) :
	return '%s %s %s' % (self.quip,self.sender,self.receiver)
    
    class Meta:	
	app_label="kwippy"	

