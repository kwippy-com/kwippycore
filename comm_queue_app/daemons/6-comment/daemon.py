#!/usr/bin/python2.5

import sys, os, time, MySQLdb
import datetime

pwdp="/home/staging/kwippyproject"

sys.path.append("/usr/lib/python2.5/site-packages/django/django")
sys.path.append("/usr/lib/python2.5/site-packages/django")
sys.path.append(pwdp)
#sys.path.append("/home/dipankar/others/kwippy/kwippyproject")


from django.core.management import setup_environ
import settings
setup_environ(settings)
from django.core.cache import cache


try:
     conn = MySQLdb.connect (host = settings.DATABASE_HOST,user = settings.DATABASE_USER,passwd = settings.DATABASE_PASSWORD,db = settings.DATABASE_NAME)
except MySQLdb.Error, e:
     print "Error %d: %s" % (e.args[0], e.args[1])
     sys.exit (1)

cursor = conn.cursor()
cursor.execute("update kwippy_comment_follower set created_at=NOW(),is_active=1 where created_at < DATE_SUB(NOW(), INTERVAL 1 DAY) ")
conn.commit()
cursor.close()
