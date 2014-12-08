from django.db import models
from django.contrib.auth.models import *

#INVITATION_TYPE_CHOICES = ((0,'Beta'), (1,'General'))
INVITATION_STATUS_CHOICES = ((0,'No action'), (1,'Awaiting Activation'), (2,'Converted'))
# Invite profile
class Invite(models.Model):
    user = models.ForeignKey(User)   
    invitee_email = models.EmailField(null = True, blank=True)   
    invite_type = models.IntegerField(default=1)
    unique_hash = models.CharField(max_length=20, unique=True)
    converted_user = models.ForeignKey(User, related_name="convered_user", null=True, default = None, blank=True)
    status = models.IntegerField(choices=INVITATION_STATUS_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
	
    def __unicode__(self) :
	return '%s' % (self.invitee_email)
    
    class Meta:	
	app_label="kwippy"	


