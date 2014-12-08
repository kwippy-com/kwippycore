from django.db import models
from django.contrib.auth.models import *
from kwippyproject.kwippy.models.quip import *

class Random_User(models.Model):
    user = models.ForeignKey(User)
    set_id = models.IntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self) :
        return '%s' % (self.user)

    class Meta:
	app_label="kwippy"	

