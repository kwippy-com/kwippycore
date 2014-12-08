from django.db import models
from django.contrib.auth.models import *

REGISTRATION_TYPE_CHOICES =((0,'IM'), (1,'Web'), (2,'Api'), (3,'Mobile'))
PROVIDER_CHOICES =((0,'Web'), (1,'Gadu-Gadu'), (2,'GTalk'), (3,'ICQ'), (4,'MSN'), (5,'MySpaceIM'), (6,'QQ'), (7,'Yahoo'), (8,'AIM'), (9,'Facebook'), (10,'Api'),(11,'Mobile'),(12,'Ping.fm'), (13,'HelloTxt'),(14,'RSS'),(15,'Pixelpipe'),('16','wordpress'))
STATUS_CHOICES = ((-1,'Blocked'), (0,'Inactive'), (1,'Active'), (3,'Deleted'))

# Account profile
class Account(models.Model):
    provider_login = models.CharField(max_length=200, default ='Web')
    other_param = models.CharField(max_length=200,blank=True,null=True,default='')
    provider = models.IntegerField(choices=PROVIDER_CHOICES, default=None, blank=True, null=True) 
    user = models.ForeignKey(User,null = True, default=None)
    registration_type = models.IntegerField(choices=REGISTRATION_TYPE_CHOICES,default=0)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # added to track status changes for a particular day..conversions from inactive accs to active

    def __unicode__(self) :
	return '%s' % (self.provider_login)
    
    class Meta:	
	app_label="kwippy"	

