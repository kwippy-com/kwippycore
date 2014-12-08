import smtplib
import sys, os, time, MySQLdb,sha,base64
import datetime

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

from django.core.mail import EmailMultiAlternatives,SMTPConnection

try:
     conn = MySQLdb.connect (host = settings.DATABASE_HOST,user = settings.DATABASE_USER,passwd = settings.DATABASE_PASSWORD,db = settings.DATABASE_NAME)
except MySQLdb.Error, e:
     print "Error %d: %s" % (e.args[0], e.args[1])
     sys.exit (1)

curr_pid = os.getpid()
current = open("/home/staging/kwippyproject/comm_queue_app/daemons/0-email/log/current", "w")
current.write(str(curr_pid))
current.close()

def logit(data):
    logger = open("/home/staging/kwippyproject/comm_queue_app/daemons/0-email/log/"+str(curr_pid)+".log", "a")
    logger.write(data + os.linesep)
    logger.close()
    
logit("Start of mailing log")
mailer_min=1
mailer_count=mailer_min
curr_msg=1
while 1:
     a = sha.new("--Kwip--"+str(mailer_count))
     password = base64.b64encode(a.digest())
     username = 'mailer'+str(mailer_count)+'@kwippy.com'
     cursor = conn.cursor()
     messages=[]
     cursor.execute("select id,obj_type,params from comm_queue_app_commd where status=0 and type=0 order by created_at limit 20")
     commands = cursor.fetchall ()
     for c in commands:
          logit("Processing : %d" % c[0])
          cursor.execute("update comm_queue_app_commd set start_at=NOW(),status=1 where id="+str(c[0]))
          conn.commit()
          param = c[2].split("||")
          logit("Number of Parameters %d" % len(param))
          if len(param)==6:
               # 0 : to, 1 : from, 2 : subject, 3 : test content, 4 : HTML content, 5 : User to be sent ID
               cursor.execute("select email from kwippy_notificationsetting where user_id="+param[5])
               logit("%s" %(param[5],))
               mail_set= cursor.fetchone()
               mail_sett=[]
               if(c[1]!=0) and mail_set:
                   mail_sett = mail_set[0].split(",")
               msg = EmailMultiAlternatives(param[2], param[3], param[1], [param[0]],headers = {'Reply-To': 'support@kwippy.com'})
               msg.attach_alternative(param[4], "text/html")
               allowed = 0
               if (c[1]==0):
                   allowed = 1
               if not mail_set:
                   allowed = 1
                   logit("not set")
               elif len(mail_sett)==0:
                   allowed = 1
               elif (mail_sett[c[1]-1] == '1'):
                   logit("%s %d" % (mail_set,c[1],))
                   allowed = 1
	       if allowed == 1:
                   messages.append(msg)
               cursor.execute("update comm_queue_app_commd set end_at=NOW(),status=2 where id="+str(c[0]))        
          else:
               cursor.execute("update comm_queue_app_commd set end_at=NOW(),status=3 where id="+str(c[0]))
     if len(messages)!=0:
	  #connection = SMTPConnection(host='smtp.gmail.com',port=587,username=username,password=password,use_tls=True)
          if mailer_count==0:
              connection = SMTPConnection(host='mail.messagingengine.com',port=587,username='mailer0@kwippy.com',password='7cuoh6',use_tls=True)
          elif mailer_count==1:
              connection = SMTPConnection(host='mail.messagingengine.com',port=587,username='mailer1@kwippy.com',password='aapio6',use_tls=True)
          elif mailer_count==2:
              connection = SMTPConnection(host='mail.messagingengine.com',port=587,username='mailer2@kwippy.com',password='jkngje',use_tls=True)
          elif mailer_count==3:
              connection = SMTPConnection(host='mail.messagingengine.com',port=587,username='mailer3@kwippy.com',password='nvyqgp',use_tls=True)
          elif mailer_count==4:
              connection = SMTPConnection(host='mail.messagingengine.com',port=587,username='mailer4@kwippy.com',password='xnuvbj',use_tls=True)
          # connection = SMTPConnection()
          logit(username)
          try:
              connection.send_messages(messages)
              curr_msg=curr_msg+len(messages)
              mailer_count=mailer_count + 1
              conn.commit()
          except smtplib.SMTPDataError:
              mailer_count=mailer_count + 1
              conn.rollback()
     if mailer_count>=5:
         mailer_count=mailer_min    
     time.sleep(60)
