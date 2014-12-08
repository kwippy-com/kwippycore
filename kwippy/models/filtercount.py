from django.db import models
from kwippyproject.kwippy.models.quip import *
from django.contrib.auth.models import *

class FilterCount(models.Model):
    fid = models.IntegerField()
    count = models.IntegerField(default=0)

    def __unicode__(self) :
	return '%d %s %s %s' % (self.type, self.subject, self.body_text, self.body_html)
    
    class Meta:	
	app_label="kwippy"	

