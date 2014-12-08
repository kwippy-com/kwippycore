import sys, os, time, MySQLdb,sha,base64
import datetime
import dbus

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

testing = 0
admin_emails = ['dipankarsarkar@gmail.com','dhingra.mayank@gmail.com','k.a.anand@gmail.com']

def send_im_msg(message,to):
    conversation = purple.PurpleConversationNew(1,37,to)
    im = purple.PurpleConversationGetImData(conversation)
    purple.PurpleConvImSend(im,message)

try:
    bus = dbus.SessionBus()
    obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
    purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")
except dbus.DBusException:
    print "Pidgin is not launched"
    sys.exit(1)

try:
     conn = MySQLdb.connect (host = settings.DATABASE_HOST,user = settings.DATABASE_USER,passwd = settings.DATABASE_PASSWORD,db = settings.DATABASE_NAME)
     #conn = MySQLdb.connect (host = 'localhost',user = 'kwippy_user1',passwd = 'helloworld69',db = 'kwippy_staging1')
except MySQLdb.Error, e:
     print "Error %d: %s" % (e.args[0], e.args[1])
     sys.exit (1)

curr_pid = os.getpid()
current = open("/home/staging/kwippyproject/comm_queue_app/daemons/4-im/log/current", "w")
current.write(str(curr_pid))
current.close()

def logit(data):
    logger = open("/home/staging/kwippyproject/comm_queue_app/daemons/4-im/log/"+str(curr_pid)+".log", "a")
    logger.write(data + os.linesep)
    logger.close()
    
logit("Start of IM log")
cursor = conn.cursor()

while 1:
    cursor.execute("select id,obj_type,params from comm_queue_app_commd where status=0 and type=4 order by created_at")
    commands = cursor.fetchall()
    for c in commands:
        logit("Processing : %d" % c[0])
        #print "Working"
        cursor.execute("update comm_queue_app_commd set start_at=NOW(),status=1 where id="+str(c[0]))
        conn.commit()
        param = c[2].split("||")
        logit("Number of Parameters %d" % len(param))
        #print "1"
        if len(param) ==3:
        # 0 : to, 1 : message, 2 : User to be sent ID
            cursor.execute("select im from kwippy_notificationsetting where id="+param[2])
            #print "2"
            im_set =  cursor.fetchone()
            #print im_set[0]
            allowed =0 
            if im_set:
                im_sett = im_set[0].split(",")
                if (c[1]==0):
                    allowed = 1
                elif (im_sett[c[1]-1] == '1'):
                    allowed = 1
            else:
                allowed = 1
            #print c[0],im_set[0]
            #print allowed
            if (allowed == 1):
                if (testing==0) or ((testing==1) and (param[0] in admin_emails)):
                   send_im_msg(param[1],param[0])
                   #print "3"
            cursor.execute("update comm_queue_app_commd set end_at=NOW(),status=2 where id="+str(c[0]))        
            conn.commit()
        time.sleep(1)
    time.sleep(10)

