"""This view will store
  email ids for beta invtes ajaxically"""
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from kwippy.models.beta_invite import Beta_Invite
from django.utils import simplejson
import re
# Create your views here.

def coming_soon(request):
  """This function will store
  email ids for beta invtes"""
  if not request.method == "POST":
    return render_to_response('signup/beta_invite.html',
                              context_instance=RequestContext(request))
  xhr = request.GET.has_key('xhr')
  response_dict = {}
  #pdb.set_trace()
  #user_ip = request.META['REMOTE_ADDR']
  user_ip = '127.0.0.1'
  user_email = request.POST.get('email', False)
  response_dict.update({'email':user_email})
  if user_email:
    new_beta = Beta_Invite(email = user_email, ip=user_ip)
    emailregex = "^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3\})(\\]?)$"
    if re.match(emailregex, user_email) == None:
      response_dict.update({'errors':'Email invalid'})
    else:
      new_beta.save()
      response_dict.update({'success':True})
  else:
    response_dict.update({'errors':'No email given'})
  if xhr:
    return HttpResponse(simplejson.dumps(response_dict),
                        mimetype='application/javascript')
  return render_to_response('signup/beta_invite.html', response_dict)
