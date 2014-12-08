from django.contrib.sitemaps import Sitemap
from kwippyproject.kwippy.models.quip import *
from kwippyproject.kwippy.models.user_profile import *

class ProfileSitemap(Sitemap):
    changefreq = "weekly"
    def items(self):
        return User_Profile.objects.all()
    def location(self,obj):
        return obj.user.username
    	
class QuipSitemap(Sitemap):
    changefreq = "always"
    def items(self):
        return Quip.objects.get_query_set().extra(tables=[],where=["""is_filtered=1"""])
 
