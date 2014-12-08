from django.db import models
from django.contrib.auth.models import *

# Fireeagle 
class Fireeagle(models.Model):
    request_token_key = models.TextField()
    request_token_secret = models.TextField()
    access_token_key = models.TextField() 
    access_token_secret = models.TextField()
    integrated = models.IntegerField(default=0)
    location = models.TextField()
    user = models.ForeignKey(User,null = True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self) :
	return '%s' % (self.request_token_key)
    
    class Meta:	
	app_label="kwippy"	

