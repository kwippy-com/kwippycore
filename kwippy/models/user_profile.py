from kwippyproject.kwippy.models.theme import *
from django.db import models
from django.contrib.auth.models import User
from djangosphinx import SphinxSearch
from kwippyproject.countries.models import Country
import datetime

# User profile
GENDER_CHOICES = ((1,'Male'), (2, 'Female'))
TENDENCY_CHOICES = ((1,'Straight'),(2,'Lesbian'), (3,'Gay'))
RSHIP_CHOICES = ((1,'Single'),(2,'Committed'), (3,'Open Relationship'))
MEDIA_STATUS_CHOICES = ((0,'Waiting'),(1,'Processing'),(2,'Success'),(3,'Failure'))
DAY_CHOICES = [(i, i) for i in range(1, 32)]
DAY_CHOICES.append((0,'Day'))
DAY_CHOICES.sort()
MONTH_CHOICES =  ((0,'Month'),(1,'January'),(2,'February'),(3,'March'),(4,'April'),(5,'May'),(6,'June'),(7,'July'),   (8,'August'),(9,'September'), (10,'October'),(11,'November'),(12,'December'))
YEAR_CHOICES = [(i, i) for i in range(1900, 2000)]
YEAR_CHOICES.append((0,'Year'))
YEAR_CHOICES.sort()


class User_Profile(models.Model): 
    user = models.ForeignKey(User, unique=True, related_name="user_profile")
    display_name = models.CharField(max_length=50,blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, blank=True, null=True)
    about_me = models.TextField(max_length=150, blank=True, null=True)
    birth_day = models.IntegerField(choices=DAY_CHOICES, blank=True, null=True, default=0)
    birth_month = models.IntegerField(choices=MONTH_CHOICES, blank=True, null=True, default=0)
    birth_year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)
    sexual_tendency = models.IntegerField(choices=TENDENCY_CHOICES, blank=True, null=True)
    relationship_status = models.IntegerField(choices=RSHIP_CHOICES, blank=True, null=True)
    location_city = models.CharField(max_length=200,blank=True, null=True)
    location_country = models.CharField(max_length=200,blank=True, null=True)
    country = models.ForeignKey(Country) 
    website = models.URLField(blank=True, null=True)
    hash = models.CharField(max_length=20, unique=True)
    media_processed = models.IntegerField(choices=MEDIA_STATUS_CHOICES, max_length = 1, default = 0, blank=True, null=True)
    picture = models.ImageField(upload_to="images",blank=True, null=True)
    picture_ver = models.IntegerField(blank=False,null=True,default=0)
    theme = models.ForeignKey(Theme,blank=True,null=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quip_total = models.IntegerField(blank=False,null=True,default=0)
    quip_repeat_total = models.IntegerField(blank=False,null=True,default=0)
    comment_count = models.IntegerField(blank=False,null=True,default=0)
    fav_count = models.IntegerField(blank=False,null=True,default=0)
    default_notification_on = models.BooleanField(default=1, blank=False, null=False)
    update_fire_eagle = models.NullBooleanField(default=0, blank=True, null=True)
    search = SphinxSearch(index="main3")
    
    def __unicode__(self) :	
        return '%s %s %s %s %s %s %s' % (self.display_name, self.about_me, self.location_city, self.location_country, self.website, self.gender, self.birth_month)
        
    class Meta:	
	app_label="kwippy"	
   
    class Admin:
	list_display = ('user', 'display_name', 'about_me', 'location_city', 'location_country', 'website')
	list_filter =  ( 'location_city', 'location_country')
	ordering = ('user',)
	search_fields = ('user',)

    def get_age(self):        
        if self.birth_year:
            year_now = datetime.datetime.now().year
            if self.birth_month:
                if self.birth_day:
                    birth_date = datetime.datetime(self.birth_year, self.birth_month, self.birth_day)
                else:
                    birth_date = datetime.datetime(self.birth_year, self.birth_month, 1)
                dt_now = datetime.datetime.now()
                age = int((dt_now - birth_date).days/365)
            else:
                age = int((year_now - self.birth_year))
        else:
            age = ""
        return age
        
