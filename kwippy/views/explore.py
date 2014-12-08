import pdb,random
from django.conf import settings
from django import template, http
from django.shortcuts import render_to_response, get_object_or_404

from kwippy.models.quip import Quip
from kwippy.models.favourite import Favourite
from kwippy.models.user_profile import User_Profile

def main(request):
    quip_count = int(Quip.objects.all().count())
    arr = []
    while len(arr)<10:        
        rand_id = int(random.random()*1000)
        #rand_id = int(random.random()*10) for local systems
        quip = Quip.objects.filter(id=rand_id)        
        #if quip and int(quip[0].account.user_id)>0:
	if quip:
            arr.append(quip[0].id)    
    rand_quips = Quip.objects.filter(id__in=arr)
    user_profile = get_object_or_404(User_Profile, user=request.user)
    return render_to_response('explore.html', {'quips':rand_quips, 'revision_number': settings.REVISION_NUMBER,
                                               'user_profile':user_profile}, context_instance=template.RequestContext(request))  
