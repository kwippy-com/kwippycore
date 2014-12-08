from django.contrib.syndication.feeds import Feed
from kwippy.models.quip import Quip

class testFeed(Feed):
    title = "Chicagocrime.org site news"
    link = "/sitenews/"
    description = "Updates on changes and additions to chicagocrime.org."

    def items(self):
        return Quip.objects.order_by('-created_at')[:5]

