from django import template
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.models import User
from kwippy.models.follower import Follower
from kwippy.models.account import Account
from kwippy.models.quip import Quip
from django.contrib.comments.models import Comment
from kwippy.views.views import queryset_to_csv
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from kwippy.views.main import get_display_name
import pdb

register = template.Library()
def do_show_flash_news(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return ShowFlashNewsNode(bits[1], bits[2])
    
def show_flash_news(parser, token):
    return do_show_flash_news(parser, token)

class ShowFlashNewsNode(Node):
    def __init__(self, var1, var2):
        self.var1 = Variable(var1)
	self.var2 = Variable(var2)
        
    def __repr__(self):
        return "<ShowFlashNewsNode>"
    
    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
	try:
            val2 = self.var2.resolve(context)
	except VariableDoesNotExist:
            val2 = None	
        user = get_object_or_404(User, id=val1)	
	last_login=val2
	new_followers=Follower.objects.filter(created_at__gt=last_login,followee=user)
	user_accounts = Account.objects.filter(user=user)
	user_quips = Quip.objects.filter(account__in=user_accounts)
	user_quips_in_csv = queryset_to_csv(user_quips,'account')
	new_comments=Comment.objects.filter(object_id__in=user_quips_in_csv,submit_date__gt=last_login).exclude(user=user)
	csv=[]
	for item in new_comments:
	    quip_id=item.object_id
	    quip = get_object_or_404(Quip, id=quip_id)
	    kwips = quip.quips_on_same_time()
	    timestamp = quip.created_at.strftime("%Y/%b/%d/%H%M%S")
	    link = user.username+'/kwips/'+timestamp.lower()
	    if len(kwips)>1:            
		link = link + '/' + str(kwips[quip.id])
	    csv.append(link)       
	if new_followers or new_comments:
	    html = ""
	    if new_comments:
		html="you have comments "
		comment_count = len(new_comments)
		for item in csv:
		    comment_count=comment_count-1
		    html = html + "<a href=\"/"+item+"/\">here</a>"
		    if comment_count!=0:
			html=html+","
		if new_followers:		
		    html= html + "<br>&&nbsp;"
	    if new_followers:		
		count = len(new_followers)
		if count==1:
		    html= html + "<a href=\"/"+new_followers[0].follower.username+"/\">" +get_display_name(new_followers[0].follower)+"</a> has started following you."  	
		else:		    
		    for follower in new_followers:
			count = count -1
			html = html + "<a href=\"/"+follower.follower.username+"/\">" +get_display_name(follower.follower)+ "</a>"
			if count!=0:
			    html=html+",&nbsp;"
		    html =  html + " have started following you."
	    html = html + "         <a href=\"javascript:void(0);\"onClick=\"hide_flash_message('update');\" >X</a>"
	else:
	    html=""  		
	return html
    
register.tag('show_flash_news',do_show_flash_news)


