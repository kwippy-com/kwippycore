from django.db import models
from django.contrib.auth.models import *
from django.contrib.comments.models import Comment

class Favourite_Comment(models.Model):
    comment = models.ForeignKey(Comment)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self) :
        return '%s %s' % (self.comment, self.user)

    class Meta:
	app_label="kwippy"	

