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
type = "comment"
type_table = "comments_comment"
fid = "3"
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
min_count=1380
while (min_count<max_count):
     cursor.execute("""select auth_user.username,comments_comment.comment,kwippy_quip.created_at,comments_comment.user_id,kwippy_quip.id from comments_comment,auth_user,kwippy_quip where comments_comment.object_id=kwippy_quip.id and comments_comment.content_type_id=19 and auth_user.id=comments_comment.user_id and comments_comment.id>=%s and comments_comment.id<%s""",(min_count,min_count+limit,))
     commands = cursor.fetchall()
     for c in commands:
          cursor.execute("""select kwippy_notificationsetting.im,auth_user.username,auth_user.id from kwippy_account,kwippy_notificationsetting,kwippy_quip,auth_user where kwippy_notificationsetting.user_id=kwippy_account.user_id and kwippy_quip.account_id=kwippy_account.id and auth_user.id=kwippy_notificationsetting.user_id and kwippy_quip.id=%s""",(c[4],))
          im_res = cursor.fetchone()
          url = c[2].strftime("%Y/%b/%d/%H%M%S")
          cursor.execute("""select count(kwippy_quip.id) from kwippy_quip,kwippy_account where kwippy_quip.created_at=%s and kwippy_quip.account_id=kwippy_account.id and kwippy_account.user_id = %s""",(c[2],im_res[2],))
          count_quip = cursor.fetchone()
          if count_quip[0]==1:
              url = url_prefix + im_res[1]+"/kwips/"+url.lower()
          else:
              url = url_prefix + im_res[1]+"/kwips/"+url.lower()+"/"+str(c[4])
          sett=im_res[0].split(",")
          cursor.execute("""select kwippy_account.provider_login from kwippy_account where kwippy_account.provider=%s and kwippy_account.user_id=%s limit 1""",(im_type,im_res[2],))
          acc = cursor.fetchone()
          if sett[0]=='1' and acc and im_res[2]!=c[3]:
              # create the message string
              mesg = c[0]+" has left a comment on your kwip:<br>"+c[1]+"<br><br>go read and reply here:<br>"+url
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
