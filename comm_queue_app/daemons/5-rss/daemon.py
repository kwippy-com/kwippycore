#!/usr/bin/python2.5

import smtplib
import sys, os, time, MySQLdb,sha,base64
import datetime
import feedparser

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

curr_pid = os.getpid()
current = open(pwdp+"/comm_queue_app/daemons/5-rss/log/current", "w")
current.write(str(curr_pid))
current.close()

def logit(data):
    logger = open(pwdp+"/comm_queue_app/daemons/5-rss/log/"+str(curr_pid)+".log", "a")
    logger.write(data + os.linesep)
    logger.close()

logit("Start of mailing log")

cursor = conn.cursor()
cursor.execute("select id,user_id,provider_login,updated_at from kwippy_account where provider=14")
commands = cursor.fetchall ()
for c in commands:
    logit("Processing : %d" % c[0])
    d = False
    try:
        d = feedparser.parse(c[2])
    except UnicodeDecodeError,e:
        pass
    #print c[2],d.bozo
    if d:
        fdate = datetime.datetime.now()
        entries = d.entries
        entries.reverse()
        for entry in entries:	  
            try:
                dtuple = entry.updated_parsed
                pdate = datetime.datetime(dtuple[0],dtuple[1],dtuple[2],dtuple[3],dtuple[4],dtuple[5])
                fdate = pdate
            except AttributeError:
                fdate = datetime.datetime.now()	    
            if pdate>c[3]:
                content = entry.title
                try:
                    content = '<b>' + entry.title + "</b> : <br/>" + entry.summary_detail.value
                except AttributeError:
                    content = entry.content[0].value
                #print entry.content[0].value
                cursor.execute("insert into kwippy_quip(user_id,account_id,original,formated,is_filtered,created_at,repeat_id,type,comment_count) values(%s,%s,%s,%s,0,%s,0,2,0)",(c[1],c[0],content.encode('ascii', 'replace'),content.encode('ascii', 'replace'),datetime.datetime.now(),))
                cursor.execute("update kwippy_user_profile set quip_total=quip_total+1 where user_id = %s",(c[1],))
                cursor.execute("update kwippy_user_profile set quip_repeat_total=quip_repeat_total+1 where user_id = %s",(c[1],))
        # update the final date
        cache_key = '%s_profilequery%d' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,c[0],)
        cache.delete(cache_key)
        cursor.execute("update kwippy_account set updated_at=%s where id=%s",(fdate,c[0],))

cursor.close()
