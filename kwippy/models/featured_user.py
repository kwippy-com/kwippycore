from django.db import models
from django.contrib.auth.models import *
from kwippyproject.kwippy.models.quip import *

class Featured_User(models.Model):
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self) :
        return '%s' % (self.user)

    class Meta:
	app_label="kwippy"	

