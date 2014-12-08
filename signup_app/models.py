"""
A model (``SignupProfile``) for storing user-registration data,
and an associated custom manager (``SignupManager``).

"""


import datetime, random, re, sha, pdb

from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from kwippyproject.kwippy.models.quip import Quip
from kwippyproject.kwippy.models.account import Account
from kwippyproject.kwippy.models.invite import Invite
from kwippyproject.kwippy.models.invite_limit import Invite_Limit
from kwippyproject.kwippy.models.user_profile import User_Profile

SHA1_RE = re.compile('^[a-f0-9]{40}$')


class SignupManager(models.Manager):
    """
    Custom manager for the ``SignupProfile`` model.
    
    The methods defined here provide shortcuts for account creation
    and activation (including generation and emailing of activation
    keys), and for cleaning out expired inactive accounts.
    
    """
    def activate_user(self, activation_key):
        """
        Validates an activation key and activates the corresponding
        ``User`` if valid.
        
        If the key is valid and has not expired, returns the ``User``
        after activating.
        
        If the key is not valid or has expired, returns ``False``.
        
        If the key is valid but the ``User`` is already active,
        returns the ``User``.
        
        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False            
            if not profile.activation_key_expired() and not profile.activation_key_used():
                user = profile.user
                user.is_active = True
                user.save()
                # code to update the invites table with convered_user's id on account activation
                invitation_hash = profile.invitation_hash
                if invitation_hash:                    
                    invite = get_object_or_404(Invite, unique_hash=invitation_hash)
                    invite_limit = Invite_Limit.objects.filter(invite=invite)
                    if len(invite_limit)==1:
                        invite_limit = invite_limit[0]
                        invite_limit.count=invite_limit.count+1
                        invite_limit.save()                    
                    if invite:                        
                        invite.status=2
                        invite.save()                
                # code to activate the corresponding account 
                account = get_object_or_404(Account, user=user, provider=0)
                account.status=1
                account.save()
                self.store_a_default_kwip(user, account)
                return user
        return False
    
    #store a default kwip from user's web account
    def store_a_default_kwip(self, user, account):        
        quip = Quip(original='hey "'+user.username+'" this is a demo kwip. kwippy lets you share your IM statuses/signatures online and have interesting conversations over them. To start kwipping integrate your Gtalk and Yahoo messenger(http://www.kwippy.com/dashboard/import) and show your creativity by writing cool, interesting and informative statuses. Using kwippy you can stay in touch with old friends and make new ones; and 100 other things you can think of.',formated='hey "'+user.username+'" this is a demo kwip. kwippy lets you <b>share your IM statuses/signatures online and have interesting conversations over them</b>. To start kwipping integrate your Gtalk and Yahoo messenger (instructions <a href="http://www.kwippy.com/dashboard/import">here</a>) and show your creativity by writing cool, interesting and informative statuses. Read <a href="http://blog.kwippy.com/2008/07/24/10-minute-guide-to-kwippy/"> kwippy guide</a> for more. You could fill in your <a href="http://www.kwippy.com/'+user.username+'/dashboard/profile/">profile info</a> so that other like minded people can find you now :)',account_id=account.id,is_filtered=1,repeat_id=0,type=1, user_id=user.id)
        quip.save()
        self.store_a_default_comment(user,quip.id)
        
    def store_a_default_comment(self, user, quip_id):
        content_type_kwip = get_object_or_404(ContentType,name='quip')
        comment = Comment(user_id=53,content_type=content_type_kwip,object_pk=quip_id,comment='hello '+user.username+', welcome to kwippy :)',site_id=1)
        comment.save()
                
    def create_inactive_user(self, username, password, email, invitation_hash=None,
                             send_email=True, profile_callback=None):
        """
        Creates a new, inactive ``User``, generates a
        ``SignupProfile`` and emails its activation key to the
        ``User``. Returns the new ``User``.
        
        To disable the email, call with ``send_email=False``.
        
        To enable creation of a custom user profile along with the
        ``User`` (e.g., the model specified in the
        ``AUTH_PROFILE_MODULE`` setting), define a function which
        knows how to create and save an instance of that model with
        appropriate default values, and pass it as the keyword
        argument ``profile_callback``. This function should accept one
        keyword argument:

        ``user``
            The ``User`` to relate the profile to.
        
        """
        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()
        
        signup_profile = self.create_profile(new_user,invitation_hash)
        # code to update the status in invites table to 1(awaiting activation)
        invite = get_object_or_404(Invite, unique_hash=invitation_hash)
        #setting the new/converted user in invites table
        invite.converted_user_id = new_user.id        
        invite.status=1
        invite.save()        
        
        #call to the function to create a corresponding entry in account table
        self.create_inactive_account(new_user)
        
        if profile_callback is not None:
            profile_callback(user=new_user)
        
        if send_email:
            from django.core.mail import send_mail
            current_site = Site.objects.get_current()
            
            subject = render_to_string('signup/activation_email_subject.txt',
                                       { 'site': current_site })
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            
            message = render_to_string('signup/activation_email.txt',
                                       { 'activation_key': signup_profile.activation_key,
                                         'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                                         'site': current_site })
            
            
        return new_user
    # to create an inactive web account for each new registered user
    def create_inactive_account(self, new_user):                
        account = Account(user_id=new_user.id,provider_login=new_user.email,provider=0,registration_type=0,status=0)
        account.save()
    
    def create_profile(self, user, invitation_hash = None):
        """
        Creates a ``SignupProfile`` for a given
        ``User``. Returns the ``SignupProfile``.
        
        The activation key for the ``SignupProfile`` will be a
        SHA1 hash, generated from a combination of the ``User``'s
        username and a random salt.
        
        """
        salt = sha.new(str(random.random())).hexdigest()[:5]
        activation_key = sha.new(salt+user.username).hexdigest()
        invitation_hash = invitation_hash
        
        return self.create(user=user,
                           activation_key=activation_key,invitation_hash=invitation_hash)
        
    def delete_expired_users(self):
        """
        Removes expired instances of ``SignupProfile`` and their
        associated ``User``s.
        
        Accounts to be deleted are identified by searching for
        instances of ``SignupProfile`` with expired activation
        keys, and then checking to see if their associated ``User``
        instances have the field ``is_active`` set to ``False``; any
        ``User`` who is both inactive and has an expired activation
        key will be deleted.
        
        It is recommended that this method be executed regularly as
        part of your routine site maintenance; the file
        ``bin/delete_expired_users.py`` in this application provides a
        standalone script, suitable for use as a cron job, which will
        call this method.
        
        Regularly clearing out accounts which have never been
        activated serves two useful purposes:
        
        1. It alleviates the ocasional need to reset a
           ``SignupProfile`` and/or re-send an activation email
           when a user does not receive or does not act upon the
           initial activation email; since the account will be
           deleted, the user will be able to simply re-signup and
           receive a new activation key.
        
        2. It prevents the possibility of a malicious user registering
           one or more accounts and never activating them (thus
           denying the use of those usernames to anyone else); since
           those accounts will be deleted, the usernames will become
           available for use again.
        
        If you have a troublesome ``User`` and wish to disable their
        account while keeping it in the database, simply delete the
        associated ``SignupProfile``; an inactive ``User`` which
        does not have an associated ``SignupProfile`` will not
        be deleted.
        
        """
        for profile in self.all():
            if profile.activation_key_expired():
                user = profile.user
                if not user.is_active:
                    user.delete()


class SignupProfile(models.Model):
    """
    A simple profile which stores an activation key for use during
    user account signup.
    
    Generally, you will not want to interact directly with instances
    of this model; the provided manager includes methods
    for creating and activating new accounts, as well as for cleaning
    out accounts which have never been activated.
    
    While it is possible to use this model as the value of the
    ``AUTH_PROFILE_MODULE`` setting, it's not recommended that you do
    so. This model's sole purpose is to store data temporarily during
    account signup and activation, and a mechanism for
    automatically creating an instance of a site-specific profile
    model is provided via the ``create_inactive_user`` on
    ``SignupManager``.
    
    """
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    activation_key = models.CharField(_('activation key'), max_length=40)
    invitation_hash = models.CharField(_('invitation code'), max_length=15, null=True, default = None, blank=True)
    
    objects = SignupManager()
    
    class Meta:
        verbose_name = _('signup profile')
        verbose_name_plural = _('signup profiles')
    
    class Admin:
        list_display = ('__str__', 'activation_key_expired')
        search_fields = ('user__username', 'user__first_name')
        
    def __unicode__(self):
        return u"Signup information for %s" % self.user
    
    def activation_key_used(self):
        
        """
        Determines whether this key has been used or not
        
        """
        if self.user.is_active:
            return True
        else:
            return False
    
    def activation_key_expired(self):
        """
        Determines whether this ``SignupProfile``'s activation
        key has expired.
        
        Returns ``True`` if the key has expired, ``False`` otherwise.
        
        Key expiration is determined by the setting
        ``ACCOUNT_ACTIVATION_DAYS``, which should be the number of
        days a key should remain valid after an account is registered.
        
        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.user.date_joined + expiration_date <= datetime.datetime.now()
    activation_key_expired.boolean = True
