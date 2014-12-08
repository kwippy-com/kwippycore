from django.forms import ModelForm
from django import forms
from django.conf import settings 
from kwippyproject.kwippy.models.user_profile import User_Profile
from kwippyproject.kwippy.models.fireeagle import Fireeagle
from kwippyproject.countries.models import Country
from kwippyproject.comm_queue_app.models import *
from StringIO import StringIO
from PIL import Image 
import pdb, datetime
import oauth
import fireeagle_api

attrs_dict_txtbox = { 'class': 'textbox' }
attrs_dict_txtarea = { 'class': 'textarea' }
GENDER_CHOICES = ((1,'Male'), (2, 'Female'))
DAY_CHOICES = [(i, i) for i in range(1, 32)]
DAY_CHOICES.append((0,'Day'))
DAY_CHOICES.sort()
MONTH_CHOICES =  ((0,'Month'),(1,'January'),(2,'February'),(3,'March'),(4,'April'),(5,'May'),(6,'June'),(7,'July'),   (8,'August'),(9,'September'), (10,'October'),(11,'November'),(12,'December'))
YEAR_CHOICES = [(i, i) for i in range(1900, 2000)]
YEAR_CHOICES.append((0,'Year'))
YEAR_CHOICES.sort()

def q(cond,on_true,on_false):
    if cond:
        result = on_true
    else:
        result = on_false
    if callable(result):
        return result()
    return result

def hs_key(request,key):
    if request.POST.has_key('update_fire_eagle'):
        return True
    else:
        return False

class User_ProfileForm(ModelForm):
    display_name =  forms.CharField(widget=forms.TextInput(attrs=attrs_dict_txtbox), required=False)
    age = forms.CharField(widget=forms.TextInput(attrs=attrs_dict_txtbox), required=False)
    gender = forms.ChoiceField(choices=(GENDER_CHOICES), widget=forms.Select(attrs=attrs_dict_txtbox), required=False)
    #about_me = forms.CharField(widget=forms.TextInput(attrs=attrs_dict_txtbox))
    #birth_date = forms.DateField(label='date', initial='2007-04-29', widget=extras.SelectDateWidget(years=range(2007, 2000, -1)))
    #birth_date = forms.DateField(label='Birth date', initial='2005-04-29', widget=SelectDateWidget(years=range(2000,1900,-1)))
    birth_day = forms.ChoiceField(choices=(DAY_CHOICES), widget=forms.Select(attrs=attrs_dict_txtbox), required=False)
    birth_month = forms.ChoiceField(choices=(MONTH_CHOICES), widget=forms.Select(attrs=attrs_dict_txtbox), required=False)
    birth_year = forms.ChoiceField(choices=(YEAR_CHOICES), widget=forms.Select(attrs=attrs_dict_txtbox), required=False)
    location_city = forms.CharField(widget=forms.TextInput(attrs=attrs_dict_txtbox), required=False)
    location_country = forms.CharField(widget=forms.TextInput(attrs=attrs_dict_txtbox), required=False)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), widget=forms.Select(attrs=attrs_dict_txtbox), required=False)
    update_fire_eagle = forms.BooleanField(required=False) 
    #picture = forms.CharField(widget=forms.TextInput(attrs=attrs_dict_txtbox))    
             # other fields that need to be customized
    class Meta:
        model = User_Profile
        exclude = ('user','hash','media_processed','picture_ver','sexual_tendency', 'relationship_status', 'website','age', 'location_country','fav_count','comment_count','quip_repeat_total','quip_total','theme','default_notification_on')
    def save(self, request):
	user_profile = User_Profile.objects.filter(user=int(request.user.id))        
        if user_profile:            
            user_profile = user_profile[0]
            user_profile.display_name = q(request.POST['display_name'],request.POST['display_name'],None)
            user_profile.birth_day =  int(request.POST['birth_day'])
            user_profile.birth_month =  int(request.POST['birth_month'])
            user_profile.birth_year =  int(request.POST['birth_year'])
            user_profile.gender = q(request.POST['gender'],request.POST['gender'], None)
            user_profile.about_me = q(request.POST['about_me'],request.POST['about_me'],'')
            #user_profile.sexual_tendency = q(request.POST['sexual_tendency'],request.POST['sexual_tendency'], None)
            #user_profile.relationship_status = q(request.POST['relationship_status'],request.POST['relationship_status'], None)
            user_profile.location_city = q(request.POST['location_city'],request.POST['location_city'],'')
            user_profile.country_id = request.POST['country']
            user_profile.update_fire_eagle = hs_key(request,'update_fire_eagle')
            if user_profile.update_fire_eagle:
                fe_obj = Fireeagle.objects.filter(user=int(request.user.id),integrated=1)
                if fe_obj:
                    fe  = fireeagle_api.FireEagle(settings.FE_CONSUMER_KEY,settings.FE_CONSUMER_SECRET)
                    access_token = oauth.OAuthToken(fe_obj[0].access_token_key,fe_obj[0].access_token_secret)
                    cc = Country.objects.filter(pk=user_profile.country_id)
                    c_str=""
                    if cc:
                        c_str = ", " + cc[0].printable_name
                    try:
                        places = fe.update(access_token,user_profile.location_city + c_str)
                    except fireeagle_api.FireEagleException,e:
                        pass
                    fe_obj[0].location = user_profile.location_city + c_str
                    fe_obj[0].save()
            #user_profile.website = q(request.POST['website'],request.POST['website'],'')
            if 'picture' in request.FILES:
                user_profile.picture_ver+=1
                im_path = settings.MEDIA_ROOT+str(request.user.id)+request.FILES['picture'].name
                im_t = Image.open(StringIO(request.FILES['picture'].read()))
                im_t.convert("RGB").save(im_path+'.jpg','jpeg')
                user_profile.picture = im_path
                comm_queue = Commd(type=1,status=0,params=im_path+".jpg||"+str(request.user.id)+"||"+str(user_profile.picture_ver))
                comm_queue.save()
            #pdb.set_trace()
            user_profile.save()
	else:
	    user_profile = User_Profile(user=request.user,display_name=request.POST['display_name'],
                                        gender=request.POST['gender'],about_me=request.POST['about_me'],location_city=request.POST['location_city'], 
                                        birth_day =  int(request.POST['birth_day']), birth_month =  int(request.POST['birth_month']),birth_year = int(request.POST['birth_year']),
                                        #                                   location_country=request.POST['location_country'],website=request.POST['website'],picture=request.FILES['picture'])
                                        location_country=request.POST['location_country'])
            user_profile.save()
        return user_profile

