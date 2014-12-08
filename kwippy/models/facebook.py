from django.db import models
from django.contrib.auth.models import *
from kwippyproject.kwippy.models.account import *

# Facebook model
class Facebook(models.Model):
    sk = models.CharField(max_length=200)
    fbid = models.CharField(max_length=200)
    registered = models.IntegerField(default=0) 
    account = models.ForeignKey(Account)
    user = models.ForeignKey(User,null = True, default=None) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self) :
	return '%s' % (self.fbid)
    
    class Meta:	
	app_label="kwippy"	

