from datetime import datetime
from django.contrib.auth.models import User
from kwippyproject.kwippy.models.quip import Quip
from kwippyproject.kwippy.models.account import Account
from kwippyproject.kwippy.models.user_profile import User_Profile
from kwippy.views.views import queryset_to_csv
from django import template
from django.template import loader
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.conf import settings
from django.core.cache import cache
import pdb

register = template.Library()

def do_displaybuzz(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return DisplayBuzzNode(bits[1], bits[2])

def displaybuzz(parser, token):
    return do_displaybuzz(parser, token)

class DisplayBuzzNode(Node):
    def __init__(self, var1, var2):
        self.var1 = Variable(var1)
        self.var2 = Variable(var2)
        
    def __repr__(self):
        return "<DisplayBuzzNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        try:
            val2 = self.var2.resolve(context)
        except VariableDoesNotExist:
            val2 = None

        user = get_object_or_404(User, username=val1)
        buzz_type = val2
        if buzz_type=='quip':
	    BUZZ_FORM = 'buzz_box.html'	
            user_accounts = Account.objects.filter(user=user)
            if user_accounts:
                accounts_list_in_csv = queryset_to_csv(user_accounts,'account')
                quips = Quip.objects.filter(account__in=accounts_list_in_csv).exclude(original='Away').order_by('-created_at')
                if quips:
                    last_kwip_time = quips[:1][0].created_at
                    time_now = datetime.now()
                    days_since_last_kwip = (time_now - last_kwip_time).days
                    if days_since_last_kwip>=2:
                        default_form = loader.get_template(BUZZ_FORM)
                        output = default_form.render(context)
                        return output
                    else:
			return "" 
                else:
                    return ""
	elif buzz_type == 'photo':
		BUZZ_FORM = 'photo_buzz.html'
                cache_key = '%s_profilequery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,user.id,)
                user_profile = cache.get(cache_key)
                if user_profile is None:
                    user_profile = get_object_or_404(User_Profile,user=user)
                    cache.set(cache_key, user_profile,86400)
		if not user_profile.picture:
                        default_form = loader.get_template(BUZZ_FORM)
                        output = default_form.render(context)
                        return output
		else:
			return ""
			
		
register.tag('displaybuzz',do_displaybuzz)
