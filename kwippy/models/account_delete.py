from django.db import models
from django.contrib.auth.models import *

class AccountDelete(models.Model):    
    user = models.ForeignKey(User, unique=True)    
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self) :
        return '%s' % (self.user)

    class Meta:
	app_label="kwippy"	   
    
