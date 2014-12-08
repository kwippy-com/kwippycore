#!/usr/bin/python2.5

import sys, os, time, MySQLdb
from PIL import Image
import datetime
import S3

#sys.path.append("G:\Dreams\django\install\django")
#sys.path.append("G:\Dreams\django\install\django\django")
#sys.path.append("G:\Dreams\django\kwippyproject")

sys.path.append("/usr/lib/python2.5/site-packages/django/django")
sys.path.append("/usr/lib/python2.5/site-packages/django")
sys.path.append("/home/staging/kwippyproject")

from django.core.management import setup_environ
import settings
setup_environ(settings)
from django.core.cache import cache


from django.core.mail import EmailMultiAlternatives,SMTPConnection

try:
     conn = MySQLdb.connect (host = settings.DATABASE_HOST,user = settings.DATABASE_USER,passwd = settings.DATABASE_PASSWORD,db = settings.DATABASE_NAME)
except MySQLdb.Error, e:
     print "Error %d: %s" % (e.args[0], e.args[1])
     sys.exit (1)

curr_pid = os.getpid()
current = open("/home/staging/kwippyproject/comm_queue_app/daemons/1-image/log/current", "w")
current.write(str(curr_pid))
current.close()

def logit(data):
    logger = open("/home/staging/kwippyproject/comm_queue_app/daemons/1-image/log/"+str(curr_pid)+".log", "a")
    logger.write(data + os.linesep)
    logger.close()

logit("Start of image log")
cursor = conn.cursor()
messages=[]
cursor.execute("select * from comm_queue_app_commd where status=0 and type=1 order by created_at limit 10")
commands = cursor.fetchall()
for c in commands:
    logit("Processing : %d" % c[0])
    cursor.execute("update comm_queue_app_commd set start_at=NOW(),status=1 where id="+str(c[0]))
    conn.commit()
    param = c[3].split("||")
    logit("Number of parameters : %d" % len(param))
    if len(param) ==3:
        cursor.execute("update kwippy_user_profile set media_processed=1 where user_id="+param[1])
        conn.commit()
        # 0 : file path , 1 : user id , 2 : picture version
        file, ext = os.path.splitext(param[0])
        ext_save = "JPEG"
        if ext.lower()=="gif":
            ext_save = "GIF"
        # This is the main thumbnail
        size = 300,300
        try:
            im = Image.open(param[0])
        except IOError,e:
            continue
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(file + "_300", ext_save)
        # Correct 
        size = 100,100
        im = Image.open(param[0])
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(file + "_100", ext_save)
        # This is the follwingthumbnail
        size1 = 64,64
        im1 = Image.open(param[0])
        im1_size = im1.size
        #print "Size : ",im1_size[0],im1_size[1]
        if im1_size[0]<im1_size[1]:
            box = 0,(im1_size[1]-im1_size[0])/2,im1_size[0],(im1_size[0]+im1_size[1])/2
            im1 = im1.crop(box)
        elif im1_size[0]>im1_size[1]:
            box = (im1_size[0]-im1_size[1])/2,0,(im1_size[0]+im1_size[1])/2,im1_size[1]
            im1 = im1.crop(box)
        im1.thumbnail(size1,Image.ANTIALIAS)
        im1.save(file + "_64", ext_save)
        size2 = 32,32
        im2 = Image.open(param[0])
        im2_size = im2.size
        if im2_size[0]<im2_size[1]:
            box = 0,(im2_size[1]-im2_size[0])/2,im2_size[0],(im2_size[0]+im2_size[1])/2
            im2 = im2.crop(box)
        elif im2_size[0]>im2_size[1]:
            box = (im2_size[0]-im2_size[1])/2,0,(im2_size[0]+im2_size[1])/2,im2_size[1]
            im2 = im2.crop(box)
        im2.thumbnail(size2, Image.ANTIALIAS)
        im2.save(file + "_32", ext_save)			   
        # upload to s3
        aws_conn = S3.AWSAuthConnection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        generator = S3.QueryStringAuthGenerator(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
        append_str = param[1]+"."+param[2]
        f=open(param[0])
        aws_conn.put(settings.BUCKET_NAME,append_str+".orig",S3.S3Object(f.read()),{ 'x-amz-acl': 'public-read' , 'content-type' : 'image/jpg' , 'cache-control' : 'max-age=315360000'})
        f.close()
        f=open(file + "_300")
        aws_conn.put(settings.BUCKET_NAME,append_str+".big",S3.S3Object(f.read()),{ 'x-amz-acl': 'public-read' , 'content-type' : 'image/jpg' , 'cache-control' : 'max-age=315360000'})
        f.close()
        f=open(file + "_100")
        aws_conn.put(settings.BUCKET_NAME,append_str+".main",S3.S3Object(f.read()),{ 'x-amz-acl': 'public-read' , 'content-type' : 'image/jpg' , 'cache-control' : 'max-age=315360000'})
        f.close()
        #os.remove(file + "_100")
        #os.remove(file + "_300")
        f=open(file + "_64")
        aws_conn.put(settings.BUCKET_NAME,append_str+".following",S3.S3Object(f.read()),{ 'x-amz-acl': 'public-read' , 'content-type' : 'image/jpg','cache-control' : 'max-age=315360000'})
        f.close()
        os.remove(file + "_64")
        f=open(file + "_32")
        aws_conn.put(settings.BUCKET_NAME,append_str+".follower",S3.S3Object(f.read()),{ 'x-amz-acl': 'public-read' , 'content-type' : 'image/jpg','cache-control' : 'max-age=315360000'})			   
        f.close()
        os.remove(file + "_32")
        os.remove(param[0])
        cursor.execute("update comm_queue_app_commd set end_at=NOW(),status=2 where id="+str(c[0]))
        cursor.execute("update kwippy_user_profile set media_processed=2 where user_id="+param[1])
        cache_key = '%s_profilequery%s' % (settings.CACHE_MIDDLEWARE_KEY_PREFIX,param[1],)
        cache.delete(cache_key)
    else:
        cursor.execute("update comm_queue_app_commd set end_at=NOW(),status=3 where id="+str(c[0]))
        cursor.execute("update kwippy_user_profile set media_processed=3 where user_id="+param[1])
    conn.commit()
cursor.close()
