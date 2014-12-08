#!/usr/bin/python2.5

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
     #conn = MySQLdb.connect (host = settings.DATABASE_HOST,user = settings.DATABASE_USER,passwd = settings.DATABASE_PASSWORD,db = settings.DATABASE_NAME)
     conn = MySQLdb.connect (host = "localhost", user = "kwippy_user" , passwd = "helloworld69" , db = "kwippy_staging")
except MySQLdb.Error, e:
     print "Error %d: %s" % (e.args[0], e.args[1])
     sys.exit (1)

path_curr = "/home/staging/kwippyproject/comm_queue_app/daemons/4-im/"
type = "kwip"
type_table = "kwippy_quip"
fid = "2"
limit = 100
im_type = "2"
url_prefix ="http://www.kwippy.com/"

curr_pid = os.getpid()
current = open(path_curr + "log/" + type, "w")
current.write(str(curr_pid))
current.close()

def logit(data):
    logger = open(path_curr+"log/"+str(curr_pid)+".log", "a")
    logger.write(data + os.linesep)
    logger.close()

def format_it(data):
    ret_str=data
    if(data.count('\n')>settings.MAX_LINE_BREAKS):
        count = 0
        for ch in data:
            if ch=='\n':
                count=count+1
                if count>settings.MAX_LINE_BREAKS:
                     ret_str=ret_str + " ..."
                     break
                ret_str=ret_str+ch
    elif(len(data)>settings.MAX_STR_LENGTH):
        ret_str = data[:settings.MAX_STR_LENGTH]
        ret_str = ret_str[:ret_str.rfind(' ')]
        ret_str = ret_str + " ..."
    else:
        ret_str = data
    return ret_str

logit("Start of mailing log")
cursor = conn.cursor()
cursor.execute("select count from kwippy_filtercount where fid="+fid)
count_obj = cursor.fetchone()
min_count = count_obj[0]
cursor.execute("select MAX(id) from "+type_table+" where repeat_id<>0")
count_obj = cursor.fetchone()
max_count = count_obj[0]
while (min_count<max_count):
     query = "select kwippy_quip.formated,kwippy_account.user_id,kwippy_user_profile.display_name,kwippy_quip.created_at,kwippy_account.id,auth_user.username,kwippy_quip.id from kwippy_quip,kwippy_account,kwippy_user_profile,auth_user where auth_user.id=kwippy_account.user_id and kwippy_quip.id>"+str(min_count)+" and kwippy_quip.id<="+str(min_count+100)+" and kwippy_quip.repeat_id=kwippy_quip.id and kwippy_quip.account_id=kwippy_account.id and kwippy_user_profile.user_id=kwippy_account.user_id order by kwippy_quip.created_at"
     cursor.execute(query) 
     commands = cursor.fetchall()
     for c in commands:
          url = c[3].strftime("%Y/%b/%d/%H%M%S")
          #cursor.execute("""select count(kwippy_quip.id) from kwippy_quip,kwippy_account where kwippy_quip.created_at=%s and kwippy_quip.account_id=kwippy_account.id and kwippy_account.user_id = %s""",(c[3],c[1],))
          #count_quip = cursor.fetchone()
          #if count_quip[0]==1:
          url = url_prefix + c[5]+"/kwips/"+url.lower()
          #else:
          #    url = url_prefix + c[5]+"/kwips/"+url.lower()+"/"+str(c[6])
          query = "select DISTINCT(kwippy_follower.follower_id),kwippy_account.provider_login,kwippy_notificationsetting.im,kwippy_follower.im_notification from kwippy_follower,kwippy_account,kwippy_notificationsetting where kwippy_follower.followee_id = "+str(c[1])+" and kwippy_account.user_id = kwippy_follower.follower_id and kwippy_notificationsetting.user_id=kwippy_follower.follower_id and kwippy_account.provider="+im_type
          cursor.execute(query)
          followers = cursor.fetchall()
          for follower in followers:
              # process the notification setting
              # depending on that insert into the table
              # logit(follower[2])
              # logit(follower[3])
              sett = follower[2].split(",")
              if ((sett[4]=='1') and (follower[3]==1)):
                  # create the message string
                  if c[2]:
                      mesg = c[2]+" posted this:<br>"+format_it(c[0])+"<br><br>go reply to this kwip here:"+url+"/?type=kwip&src=im"
                  else:
                      mesg = c[5]+" posted this:<br>"+format_it(c[0])+"<br><br>go reply to this kwip here:"+url+"/?type=kwip&src=im"
                  params = follower[1]+"||"+mesg+"||"+str(follower[0])
                  cursor.execute("""insert into comm_queue_app_commd(type,obj_type,params,status,created_at) values(4,5,%s,0,NOW())""",(params,))
          conn.commit()
     min_count+=limit
cursor.execute("""update kwippy_filtercount set count=%s where fid=%s""",(max_count,fid,))
cursor.close()
