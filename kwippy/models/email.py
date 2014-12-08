from django.db import models

#EMAIL_TYPE_CHOICES =((1,'Beta Invite'), (2,'Invite'), (3,'Account Activation'), (4,'Forgot Password'), (5,'Forgot Password'), (6,'Comment on Quip'))

# Email profile
class Email(models.Model):    
    type = models.CharField(max_length=30)
    subject = models.CharField(max_length=100)
    body_text = models.CharField(max_length=1000)
    body_html = models.CharField(max_length=1000)    

    def __unicode__(self) :
	return '%d %s %s %s' % (self.type, self.subject, self.body_text, self.body_html)
    
    class Meta:	
	app_label="kwippy"	
