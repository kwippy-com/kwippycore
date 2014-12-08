from django.db import models
from django.contrib.auth.models import *
from kwippyproject.kwippy.models.quip import *

class Favourite(models.Model):
    quip = models.ForeignKey(Quip)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self) :
        return '%s' % (self.quip)

    class Meta:
	app_label="kwippy"	
