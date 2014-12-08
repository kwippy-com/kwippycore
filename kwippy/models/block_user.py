from django.db import models
from django.contrib.auth.models import *

class Block_User(models.Model):
    good_guy = models.ForeignKey(User,related_name='good_guy')
    bad_guy = models.ForeignKey(User,related_name='bad_guy')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self) :	
        return '%s %s' % (self.good_guy,self.bad_guy)
  
    class Meta:
	app_label="kwippy"	
