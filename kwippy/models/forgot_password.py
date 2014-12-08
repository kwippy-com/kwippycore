from django.db import models
from django.contrib.auth.models import *

class ForgotPassword(models.Model):
    user = models.ForeignKey(User)
    reset_link = models.CharField(max_length=50)
    is_active = models.BooleanField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
	app_label="kwippy"
	

