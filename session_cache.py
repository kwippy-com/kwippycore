from django.core.cache.backends.memcached import CacheClass
from django.conf import settings

scheme, rest = settings.SESSION_CACHE.split(':', 1)
host = rest[2:-1]
cache = CacheClass(host,{})

