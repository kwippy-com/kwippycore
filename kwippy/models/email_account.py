from django.db import models
from django.contrib.auth.models import *

STATUS_CHOICES = ((0,'Inactive'), (1,'Active'))

# Account profile
class Email_Account(models.Model):
    email = models.CharField(max_length=200, null = False, blank=False)
    user = models.ForeignKey(User)
    code = models.CharField(max_length=10)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self) :
	return '%s' % (self.email)
    
    class Meta:	
	app_label="kwippy"	
