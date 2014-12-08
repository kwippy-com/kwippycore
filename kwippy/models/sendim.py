from django.db import models
from django.contrib.auth.models import *

class Sendim(models.Model):    
    message = models.TextField()
    provider_login = models.CharField(max_length=200)
    provider = models.IntegerField(default=0)

    def __unicode__(self) :
	return '%s %s %d' % (self.message, self.provider, self.provider_login)
    
    class Meta:	
	app_label="kwippy"	

