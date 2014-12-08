from django.db import models
from django.contrib import admin 
from django.contrib.auth.models import *
from django.newforms import ModelForm


def q(cond,on_true,on_false):
    if cond:
        result = on_true
    else:
        result = on_false
    if callable(result):
        return result()
    return result

SENT_EMAIL_TYPE_CHOICES = ((0, 'No mail sent'), (1, 'Thanks mail sent'), (2, 'Invite sent'))
# Beta Invite profile
class Beta_Invite(models.Model):
    email = models.EmailField(blank=False) 
    sent_email_status = models.IntegerField(choices=SENT_EMAIL_TYPE_CHOICES, default = 0 , verbose_name="status of emails sent to this mail id during beta testing")
    user = models.ForeignKey(User, null = True, default = None)  
    ip = models.IPAddressField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self) :
	return '%s %s' % (self.email, self.ip)

    class Meta:
	app_label="kwippy" 


class Code_Type(models.Model):
    code_type = models.CharField(max_length=20, unique=True)
    type_description = models.CharField(max_length=100)

    def __unicode__(self) :
	return '%s %s' % (self.code_type, self.type_description)

    class Meta:
	app_label="kwippy"	    

class Code_Value(models.Model):
    code_value = models.CharField(max_length=20, unique=True)
    value_description = models.CharField(max_length=100)

    def __unicode__(self) :
	return '%s %s' % (self.code_value, self.value_description)

    class Meta:
	app_label="kwippy"


class Code_Type_Value(models.Model):
    code_type  = models.ForeignKey(Code_Type, related_name="code type id")
    code_value = models.ForeignKey(Code_Value, related_name="code value id")

    def __unicode__(self) :
	return '%d %d' % (self.code_type_id, self.code_value_id)

    class Meta:
	app_label="kwippy"
	
class SupportedIMs(models.Model):
    display_name = models.CharField(max_length=35, unique=True)
    name = models.CharField(max_length=100,   unique=True)
    buddy =  models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self) :
        return '%s %s' % (self.display_name, self.buddy)

    class Meta:
	app_label="kwippy"	
	