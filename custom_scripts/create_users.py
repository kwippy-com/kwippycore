import urllib, urllib2, MySQLdb
site = 'http://localhost:1000'

conn = MySQLdb.connect(host='localhost',user='root',passwd='mayank',db='kwippy')
cur = conn.cursor()
sql_1 = "select * from kwippy_invite where status=0"
no_of_invites = int(cur.execute(sql_1))
values = {'password1':'auto', 'password2':'auto'}
#for i in range(no_of_invites):
invites = cur.fetchone()
values['username']='auto'+str(invites[0])
values['email']='auto'+str(invites[0])+'@auto'+str(invites[0])+'.com'
data = urllib.urlencode(values)
url = site+'/signup/'+str(invites[4])+'/'    
req = urllib2.Request(url,data)
try:
    handle = urllib2.urlopen (req)
except IOError:    
    print 'Something went wrong'        
else:
    print 'acc_created'
    cur.close()
    conn.close()
    conn = MySQLdb.connect(host='localhost',user='root',passwd='mayank',db='kwippy')
    cur = conn.cursor()
    sql_2 = "select * from signup_app_signupprofile order by id desc limit 1"
    print sql_2
    cur.execute(sql_2)
    signup_profile = cur.fetchone()
    print signup_profile
    act_link = signup_profile[2]
    print act_link
    url = site+'/activate/'+str(act_link)+'/'
    print url
    req = urllib2.Request(url)
    try:
        handle = urllib2.urlopen (req)
    except IOError:    
        print 'Something went wrong'        
    else:
        print 'acc_activated'      

    cur.close()
    conn.close()