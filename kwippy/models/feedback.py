from django.db import models
from django.contrib.auth.models import *

# Follower profile
class Feedback(models.Model):    
    user = models.ForeignKey(User,related_name="feedbacker")
    page =  models.CharField(max_length=30)
    text = models.CharField(max_length = 1000)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self) :	
        return '%s %s' % (self.user, self.page)
  
    class Meta:
	app_label="kwippy"	
	 
