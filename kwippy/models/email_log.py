from django.db import models
from django.contrib.auth.models import User

EMAIL_TYPE_CHOICES =((1,'birthday'),)

# Email Log profile
class Email_Log(models.Model):    
    type = models.IntegerField(choices=EMAIL_TYPE_CHOICES, blank=True, null=True)
    receiver = models.ForeignKey(User, related_name="email_receiver")
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self) :
	return '%d %s' % (self.type, self.receiver)
    
    class Meta:	
	app_label="kwippy"	
