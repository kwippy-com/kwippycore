from django.db import models
from django.contrib.auth.models import *

class PageSetting(models.Model):    
    user = models.ForeignKey(User, unique=True)    
    show_repeat = models.BooleanField(default=0, blank=False, null=False)

    def __unicode__(self) :
        return '%s %d' % (self.user, self.show_repeat)

    class Meta:
	app_label="kwippy"	   

