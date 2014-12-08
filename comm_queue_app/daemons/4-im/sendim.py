import sys, os, time, MySQLdb,dbus
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
     # conn = MySQLdb.connect (host = settings.DATABASE_HOST,user = settings.DATABASE_USER,passwd = settings.DATABASE_PASSWORD,db = settings.DATABASE_NAME)
     conn = MySQLdb.connect (host = "localhost", user = "root" , passwd = "helloworld69" , db = "kwippy_staging1")
except MySQLdb.Error, e:
     print "Error %d: %s" % (e.args[0], e.args[1])
     sys.exit (1)

path_curr = "/home/staging/kwippyproject/comm_queue_app/daemons/4-im/"
type_table = "kwippy_sendimr"
fid = "6"
limit = 100
im_type = "2"
testing = 1

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
     cursor.execute("""select message,provider_login from kwippy_sendim where kwippy_sendim.id>=%s and kwippy_sendim.id<%s and provider_type=%s""",(min_count,min_count+limit,im_type,))
     commands = cursor.fetchall()
     for c in commands:
         send_im_msg(c[0],c[1])
     min_count+=limit
cursor.execute("""update kwippy_filtercount set count=%s where fid=%s""",(max_count,fid,))
cursor.close()
