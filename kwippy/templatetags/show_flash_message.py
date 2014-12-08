from django import template
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.models import User
from kwippyproject.kwippy.models.account import Account
from django.shortcuts import get_object_or_404
from kwippy.views.main import get_display_name
from django.template import Node, NodeList, Template, Context, Variable
from kwippy.views.main import get_display_name
from django.conf import settings

register = template.Library()
def do_show_flash_message(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return ShowFlashMessageNode(bits[1], bits[2], bits[3])
    
def show_flash_message(parser, token):
    return do_show_flash_message(parser, token)

class ShowFlashMessageNode(Node):
    def __init__(self, var1, var2, var3):
        self.var1 = Variable(var1)
        self.var2 = Variable(var2)
	self.var3 = Variable(var3)
        
    def __repr__(self):
        return "<ShowFlashMessageNode>"
    
    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        try:
            val2 = self.var2.resolve(context)
        except VariableDoesNotExist:
            val2 = None
	try:
            val3 = self.var3.resolve(context)
        except VariableDoesNotExist:
            val3 = None
        user = get_object_or_404(User, id=val1)
	account = Account.objects.filter(user=user)
	html=""
	if val2=='first_login':
	    if val3!='mypage':
		if val3=='import' and len(account)==1:
		    html="<div>archive your Gtalk statuses, do it now or later.<a href=\"/everyone/active?src=importskip\" > Skip>></a></div>"  
		#elif val3=='profile' and user.get_profile().updated_at==user.date_joined:
                elif val3=='profile':                    
           	    html="<div>fill your personal details here, or <a href=\"/"+str(user.username)+"/dashboard/import?src=profileskip\">skip>></a> and do it later</div>"
           	elif val3 =='invite':                    
		    html="<div>find & invite your twitter friends here, or <a href=\"/"+str(user.username)+"/dashboard/profile/?src=inviteskip\">skip>></a> and do it later</div>"  
	    else:
		if len(account)==1:
		    html="<div>why don\'t you integrate your Gtalk statuses to this page, do it here <a href=\"/"+str(user.username)+"/dashboard/import\"> here>></a>  &nbsp;&nbsp;&nbsp;<a href=\"javascript:void(0);\"onClick=\"hide_flash_message('perm')\"; >X</a></div>"  		
	    return html
	else:
	    return ""
    
register.tag('show_flash_message',do_show_flash_message)


