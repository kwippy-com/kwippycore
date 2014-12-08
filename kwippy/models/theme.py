from django.db import models

# Themes 
class Theme(models.Model):
    params = models.TextField() 
    name = models.TextField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    version = models.IntegerField(default=0)

    def __unicode__(self) :
	return '%s' % (self.params)
    
    class Meta:	
	app_label="kwippy"	

