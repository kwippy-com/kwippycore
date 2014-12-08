from django.db import models

class ContactUs(models.Model):
    senders_email = models.EmailField(blank=True, null=True)
    message = models.TextField()    
    senders_user_id = models.IntegerField(blank=True, null=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
	app_label="kwippy"
    
