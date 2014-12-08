from django.db import models
from django.contrib.auth.models import *
from kwippyproject.kwippy.models.quip import *

class Featured_Kwip(models.Model):
    quip = models.ForeignKey(Quip)
    user = models.ForeignKey(User)
    email_sent = models.BooleanField(default=0, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self) :
        return '%s %s %d' % (self.quip, self.user, self.email_sent)

    class Meta:
	app_label="kwippy"	

