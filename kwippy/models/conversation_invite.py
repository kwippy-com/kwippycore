from django.db import models
from django.contrib.auth.models import User
from kwippyproject.kwippy.models.quip import Quip

# Invite profile
class ConversationInvite(models.Model):
    quip = models.ForeignKey(Quip)
    sender = models.ForeignKey(User,related_name="conv_invite_sender")
    receiver = models.ForeignKey(User,related_name="conv_invite_receiver")
    comment_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self) :
	return '%s %s %s' % (self.quip,self.sender,self.receiver)
    
    class Meta:	
	app_label="kwippy"	

