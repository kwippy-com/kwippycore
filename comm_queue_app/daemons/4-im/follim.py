import sys, os, time, MySQLdb
from datetime import datetime

#sys.path.append("G:\Dreams\django\install\django")
#sys.path.append("G:\Dreams\django\install\django\django")
#sys.path.append("G:\Dreams\django\kwippyproject")

sys.path.append("/usr/lib/python2.5/site-packages/django/django")
sys.path.append("/usr/lib/python2.5/site-packages/django")
sys.path.append("/home/staging/kwippyproject")
#sys.path.append("/home/dipankar/kwippy-svn/svn/trunk/kwippyproject")

from django.core.management import setup_environ
import settings
setup_environ(settings)

try:
     # conn = MySQLdb.connect (host = settings.DATABASE_HOST,user = settings.DATABASE_USER,passwd = settings.DATABASE_PASSWORD,db = settings.DATABASE_NAME)
     conn = MySQLdb.connect (host = "localhost", user = "root" , passwd = "helloworld69" , db = "kwippy_staging1")
except MySQLdb.Error, e:
     print "Error %d: %s" % (e.args[0], e.args[1])
     sys.exit (1)

path_curr = "/home/staging/kwippyproject/comm_queue_app/daemons/4-im/"
type = "follower"
type_table = "kwippy_follower"
fid = "4"
limit = 100
im_type = "2"
url_prefix ="http://www.kwippy.com/"
testing = 1
test_emails = ["dipankarsarkarsarkar@gmail.com","k.a.anand@gmail.com","dhingra.mayank@gmail.com"]

curr_pid = os.getpid()
current = open(path_curr + "log/" + type, "w")
current.write(str(curr_pid))
current.close()

def logit(data):
    logger = open(path_curr+"log/"+str(curr_pid)+".log", "a")
    logger.write(data + os.linesep)
    logger.close()
    
logit("Start of mailing log")
cursor = conn.cursor()
cursor.execute("select count from kwippy_filtercount where fid="+fid)
count_obj = cursor.fetchone()
min_count = count_obj[0]
cursor.execute("select MAX(id) from "+type_table)
count_obj = cursor.fetchone()
max_count = count_obj[0]
while (min_count<max_count):
     cursor.execute("""select kwippy_follower.followee_id,auth_user.username,kwippy_user_profile.display_name from kwippy_user_profile,kwippy_follower,auth_user where kwippy_user_profile.user_id=auth_user.id and auth_user.id=kwippy_follower.follower_id and kwippy_follower.id>=%s and kwippy_follower.id<%s""",(min_count,min_count+limit,))
     commands = cursor.fetchall()
     for c in commands:
          cursor.execute("""select DISTINCT(kwippy_account.provider_login),kwippy_notificationsetting.im from kwippy_account,kwippy_notificationsetting where kwippy_notificationsetting.user_id=%s and kwippy_account.provider=%s and kwippy_account.user_id=%s LIMIT 1""",(c[0],im_type,c[0],))
          acc = cursor.fetchone()
          if acc:
              sett = acc[1].split(",")
              if sett[1]=='1':
                  # create the message string
                  mesg = "you have got a new follower :)<br>"+c[2]+" so likes what you kwip that "+c[2]+"'s started following your kwips.<br><br>you could checkout "+c[2]+"'s page too:"+url_prefix+c[1]
                  # if testing then check
                  if testing==0:
                      cursor.execute("""insert into kwippy_sendim(message,provider_login,provider) values(%s,%s,%s)""",(mesg,acc[0],im_type,))
                  else:
                      if acc[0] in test_emails:
                          cursor.execute("""insert into kwippy_sendim(message,provider_login,provider) values(%s,%s,%s)""",(mesg,acc[0],im_type,))
              conn.commit()
     min_count+=limit
cursor.execute("""update kwippy_filtercount set count=%s where fid=%s""",(max_count,fid,))
cursor.close()
