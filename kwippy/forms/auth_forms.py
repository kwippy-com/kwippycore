from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.sites.models import Site
from django.template import Context, loader
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
import pdb,sha,random,os
from django.conf import settings
from django.utils.translation import ugettext_lazy as _, ugettext

attrs_dict_txtbox = { 'class': 'textbox' }

class AuthenticationForm(forms.Form):
    email = forms.CharField(label=_('email'),max_length = 75,required=True)
    #password = forms.CharField(label=_('password'),min_length = 6, required=True,widget = forms.PasswordInput(attrs=attrs_dict_txtbox) )
    password = forms.CharField(label=_('password'),min_length = 6, required=True, widget = forms.PasswordInput)
    Remember = forms.BooleanField(label=_('Remember'),required=False,widget = forms.CheckboxInput())
    user = None
    
    def clean(self):
       if self._errors: return
       from django.contrib.auth import login, authenticate
       email_user = User.objects.filter(email=self.data['email'])
       if not email_user:
           username = self.data['email']
       else:
	   username = email_user[0].username
       user = authenticate(username=username,password=self.data['password'])
       if user is not None:
           if user.is_active:
               self.user = user
           else:
               raise forms.ValidationError(ugettext('This account is currently inactive. Please contact the administrator if you believe this to be in error.'))
       else:
           raise forms.ValidationError(ugettext('The username and password you specified are not valid.'))

    def login(self, request):
	from django.contrib.auth import login
	if self.is_valid():
	    login(request, self.user)
	    return True
	return False

    def hasCookiesEnabled(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(ugettext("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))

class PasswordResetForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs=attrs_dict_txtbox))

    def clean_email(self):
        """
        Verify that the email and the user exists
        """
        email = self.cleaned_data.get("email")
        try:
            User.objects.get(email=email)
        except:
            raise forms.ValidationError(ugettext("There's no user with that e-mail"))

        return email

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(min_length = 6, required=True,widget = forms.PasswordInput(attrs=attrs_dict_txtbox) )
    new_password1 = forms.CharField(min_length = 6, required=True,widget = forms.PasswordInput(attrs=attrs_dict_txtbox) )
    new_password2 = forms.CharField(min_length = 6, required=True,widget = forms.PasswordInput(attrs=attrs_dict_txtbox) )
    
    def clean(self):
        if self._errors:
            return
        if not self.user.check_password(self.cleaned_data.get('old_password')):
            raise forms.ValidationError(ugettext("Your old password was entered incorrectly. Please enter it again."))
	
    def set_user(self, user):
        self.user = user

    def save(self, new_data):
        "Saves the new password."
        self.user.set_password(new_data['new_password1'])
        self.user.save()

class ForgotPasswordForm(forms.Form):
   newpass1 = forms.CharField( min_length = 6, widget = forms.PasswordInput(attrs=attrs_dict_txtbox) )
   newpass2 = forms.CharField( min_length = 6, widget = forms.PasswordInput(attrs=attrs_dict_txtbox) )

   def clean_newpass2(self):
       """
       Verify the equality of the two passwords
       """

       if self.cleaned_data.get("newpass1") and self.cleaned_data.get("newpass1") == self.cleaned_data.get("newpass2"):
           return self.cleaned_data.get("newpass2")
       else:
           raise forms.ValidationError(_("The passwords inserted are different."))

   def save(self, user):
       "Saves the new password."
       user.set_password(self.cleaned_data.get('newpass1'))
       user.save()

