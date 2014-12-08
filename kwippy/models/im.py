from django.db import models


# Email profile
class IM(models.Model):    
    type = models.CharField(max_length=30)
    body = models.CharField(max_length=1000)

    def __unicode__(self) :
	return '%d %s' % (self.type, self.body)
    
    class Meta:	
	app_label="kwippy"	

