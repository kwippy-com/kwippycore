from django.db import models
from django.contrib import admin
from django.contrib.auth.models import *

SENT_EMAIL_TYPE_CHOICES = ((0, 'No mail sent'), (1, 'Thanks mail sent'), (2, 'Invite sent'))

# Beta Invite profile
class Beta_Invite(models.Model):
    email = models.EmailField(blank=False) 
    sent_email_status = models.IntegerField(choices=SENT_EMAIL_TYPE_CHOICES, default = 0 , verbose_name="status of emails sent to this mail id during beta testing")
    user = models.ForeignKey(User, null = True, default = None)  
    ip = models.IPAddressField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self) :
	return '%s %s' % (self.email, self.ip)

    class Meta:
	app_label="kwippy" 

