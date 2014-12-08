"""This view will contain functions
  for all the static pages"""  
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def kwippy_help(request):
  """redirect to help page"""
  return render_to_response('static_pages/help.html', context_instance=RequestContext(request))

def tos(request):
  """redirect to TOS page"""
  return render_to_response('static_pages/tos.html', context_instance=RequestContext(request))

@login_required
def privacy(request):
  """redirect to privacy page"""
  return render_to_response('static_pages/privacy.html', context_instance=RequestContext(request))

def team(request):
  """redirect to team page"""
  return render_to_response('static_pages/team.html', context_instance=RequestContext(request))

def about(request):
    return render_to_response('static_pages/about.html', context_instance=RequestContext(request))

def solutions(request):
    return render_to_response('static_pages/solutions.html', context_instance=RequestContext(request))
  
def extras(request):
  """redirect to team page"""
  return render_to_response('static_pages/extras.html', context_instance=RequestContext(request))
