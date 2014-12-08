from kwippyproject.kwippy.models.account import Account
from django.contrib.auth.models import *
from django import template
from django.shortcuts import get_object_or_404
from django.template import Node, NodeList, Template, Context, Variable
from django.conf import settings
import pdb

# This is used in only console .... no optimizations thats why
register = template.Library()

def do_displayaccountstatus(parser, token):
    bits = list(token.split_contents())
    nodelist = NodeList()
    return DisplayAccountStatusNode(bits[1])

def displayaccountstatus(parser, token):
    return do_displayinviter(parser, token)

class DisplayAccountStatusNode(Node):
    def __init__(self, var1):
        self.var1 = Variable(var1)
        
    def __repr__(self):
        return "<DisplayAccountStatusNode>"

    def render(self, context):
        try:
            val1 = self.var1.resolve(context)
        except VariableDoesNotExist:
            val1 = None
        user = User.objects.filter(id=val1)
        if user:
            user=user[0]
            account = Account.objects.filter(provider_login=str(user.email),provider=2)
            if account:
                if account[0].status and account[0].user_id>0:
                    return "Integrated"
                else:
                    return "Added"
            else:
                return "Not Added"
        
register.tag('displayaccountstatus',do_displayaccountstatus)
