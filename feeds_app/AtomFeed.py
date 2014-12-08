from kwippyproject.feeds_app.RSSFeed import PublicTimelineFeed,ActivePublicTimelineFeed, FriendsTimelineFeed,ActiveFriendsTimelineFeed,UserTimelineFeed,RepliesFeed,FriendsFeed,FollowersFeed,FavoriteFeed
from django.utils.feedgenerator import Atom1Feed

class AtomPublicTimelineFeed(PublicTimelineFeed):
    feed_type = Atom1Feed
    subtitle = PublicTimelineFeed.description
    
class ActiveAtomPublicTimelineFeed(PublicTimelineFeed):
    feed_type = Atom1Feed
    subtitle = ActivePublicTimelineFeed.description

class AtomFriendsTimelineFeed(FriendsTimelineFeed):
    feed_type = Atom1Feed
    subtitle = FriendsTimelineFeed.description

class ActiveAtomFriendsTimelineFeed(FriendsTimelineFeed):
    feed_type = Atom1Feed
    subtitle = ActiveFriendsTimelineFeed.description
    
class AtomUserTimelineFeed(UserTimelineFeed):
    feed_type = Atom1Feed
    subtitle = UserTimelineFeed.description
    
class AtomRepliesFeed(RepliesFeed):
    feed_type = Atom1Feed
    subtitle = RepliesFeed.description
    
class AtomFriendsFeed(FriendsFeed):
    feed_type = Atom1Feed
    subtitle = FriendsFeed.description
    
class AtomFollowersFeed(FollowersFeed):
    feed_type = Atom1Feed
    subtitle = FollowersFeed.description
    
class AtomFavoriteFeed(FavoriteFeed):
    feed_type = Atom1Feed
    subtitle = FavoriteFeed.description
    
