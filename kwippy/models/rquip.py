from django.db import models
from kwippyproject.kwippy.models.quip import *
from kwippyproject.kwippy.models.account import *
from django.contrib.auth.models import *

class Rquip(models.Model):    
    hash = models.CharField(max_length=45,db_index=True)
    first = models.ForeignKey(Quip)
    user = models.ForeignKey(User)
    acc = models.ForeignKey(Account)
    count = models.IntegerField(default=0)

    def __unicode__(self) :
	return '%s %s %s %s %d' % (self.hash, self.first, self.user, self.acc, self.count)
    
    class Meta:	
	app_label="kwippy"	

