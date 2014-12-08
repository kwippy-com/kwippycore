"""
Forms and validation code for user signup.

"""
import re
from django.conf import settings
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from signup_app.models import SignupProfile

alnum_re = re.compile(r'^\w+$')

# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = { 'class': 'required textbox' }
test_dict = { 'class': 'required textbox' }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs=attrs_dict),
                               label=_(u'username'))    
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict),
                                label=_(u'password'))
    

class SignupForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the request username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should either preserve the base ``save()`` or implement
    a ``save()`` which accepts the ``profile_callback`` keyword
    argument and passes it through to
    ``SignupProfile.objects.create_inactive_user()``.
    
    """
    username = forms.CharField(max_length=30,
                               widget=forms.TextInput(attrs=test_dict),
                               label=_(u'username'))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_(u'email address'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict),
                                label=_(u'password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict),
                                label=_(u'password (again)'))
    
    def clean_username(self):
        """
        Validates that the username is alphanumeric and is not already
        in use.
        
        """
        if len(self.cleaned_data['username'])<3 or len(self.cleaned_data['username'])>18:
            raise forms.ValidationError(_(u'Username should contain minimum 3 characters and maximum 18 characters'))
        if not alnum_re.search(self.cleaned_data['username']):
            raise forms.ValidationError(_(u'Usernames can only contain letters, numbers and underscores'))
        try:            
            is_user_reserved = settings.RESERVED_WORDS_LIST.count(self.cleaned_data['username'])
            if is_user_reserved:
                user = User.objects.all()[:1]
            else:
                user = User.objects.get(username__exact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(u'This username is already taken. Please choose another.'))
    
    def clean_password2(self):
        """
        Validates that the two password inputs match.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] == self.cleaned_data['password2']:
                return self.cleaned_data['password2']
            raise forms.ValidationError(_(u'You must type the same password each time'))
    
    def save(self, invitation_hash=None, profile_callback=None):
        """
        Creates the new ``User`` and ``SignupProfile``, and
        returns the ``User``.
        
        This is essentially a light wrapper around
        ``SignupProfile.objects.create_inactive_user()``,
        feeding it the form data and a profile callback (see the
        documentation on ``create_inactive_user()`` for details) if
        supplied.
        
        """
        new_user = SignupProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
                                                                    password=self.cleaned_data['password1'],
                                                                    email=self.cleaned_data['email'],
                                                                    invitation_hash = invitation_hash,
                                                                    send_email = False,
                                                                    profile_callback=profile_callback)
        return new_user


class SignupFormTermsOfService(SignupForm):
    attrs_dict = { 'class': 'required' }
    """
    Subclass of ``SignupForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.
    
    """
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u'I have read and agree to the Terms of Service'))
    
    def clean_tos(self):
        """
        Validates that the user accepted the Terms of Service.
        
        """
        if self.cleaned_data.get('tos', False):
            return self.cleaned_data['tos']
        raise forms.ValidationError(_(u'You must agree to the terms to signup'))


class SignupFormUniqueEmail(SignupFormTermsOfService):
    """
    Subclass of ``SignupForm`` which enforces uniqueness of
    email addresses.
    
    """
    def clean_email(self):
        """
        Validates that the supplied email address is unique for the
        site.
        
        """
        try:
            user = User.objects.get(email__exact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_(u'This email address is already in use. Please supply a different email address.'))


class SignupFormNoFreeEmail(SignupForm):
    """
    Subclass of ``SignupForm`` which disallows signup with
    email addresses from popular free webmail services; moderately
    useful for preventing automated spam signup.
    
    To change the list of banned domains, subclass this form and
    override the attribute ``bad_domains``.
    
    """
    bad_domains = ['aim.com', 'aol.com', 'email.com', 'gmail.com',
                   'googlemail.com', 'hotmail.com', 'hushmail.com',
                   'msn.com', 'mail.ru', 'mailinator.com', 'live.com']
    
    def clean_email(self):
        """
        Checks the supplied email address against a list of known free
        webmail domains.
        
        """
        email_domain = self.cleaned_data['email'].split('@')[1]
        if email_domain in self.bad_domains:
            raise forms.ValidationError(_(u'Signup using free email addresses is prohibited. Please supply a different email address.'))
        return self.cleaned_data['email']
