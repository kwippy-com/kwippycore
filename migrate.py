import sys, os, time, re, MySQLdb
import datetime

# get the settings

#sys.path.append("G:\Dreams\django\install\django")
#sys.path.append("G:\Dreams\django\install\django\django")
#sys.path.append("G:\Dreams\django\kwippyproject")

sys.path.append("/usr/lib/python2.5/site-packages/django/django")
sys.path.append("/usr/lib/python2.5/site-packages/django")
sys.path.append("/home/staging1/kwippyproject")

from django.core.management import setup_environ
import settings

setup_environ(settings)

# got the current directory
currentdir = os.curdir
# migration directory
migratedir = os.path.join(currentdir,"migrations")
sys.path.append(migratedir)
# list the files there
files = os.listdir(migratedir)
# create a filter
test = re.compile("\.py$", re.IGNORECASE)
# use filter on files
files = filter(test.search, files)
# using a lambda function to get the filenames
filenameToModuleName = lambda f: os.path.splitext(f)[0]
# get all the filenames with the number prepended
halfNames = map(filenameToModuleName, files)

try:
    conn = MySQLdb.connect (host = settings.DATABASE_HOST,user = settings.DATABASE_USER,passwd = settings.DATABASE_PASSWORD,db = settings.DATABASE_NAME)
except MySQLdb.Error, e:
    print "Error in connection %d: %s" % (e.args[0], e.args[1])
    sys.exit (1)

def exist(num):
    cursor = conn.cursor()
    cursor.execute("select * from dbmigration_migrationhistory where migration="+num)
    if cursor.rowcount == 1:
        return False
    return True

new_max = max
for name in halfNames:
    # process the name
    splitname = re.findall("([A-Za-z]+)([0-9]+)",name)[0]
    print "Module name: ",name
    if exist(splitname[1]):
        module_stuff = __import__(name)
        hw = getattr(module_stuff,splitname[0])
        hw.up(conn)
        cursor = conn.cursor()
        cursor.execute("insert into dbmigration_migrationhistory(migration,created_at) values("+splitname[1]+",NOW())")
        conn.commit()
