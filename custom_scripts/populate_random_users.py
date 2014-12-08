import urllib, urllib2, MySQLdb
site = 'http://localhost:1000'

conn = MySQLdb.connect(host='localhost',user='root',passwd='mayank',db='kwippy_staging')
cur = conn.cursor()
sql_1 = "select * from kwippy_user_profile where media_processed=2 and user_id not in (1,53)"
no_of_profiles = cur.execute(sql_1)
print no_of_profiles
#for i in range(no_of_invites):
count = 0
profiles = cur.fetchall()
print profiles
for profile in profiles:
    set = count/9 + 1
    print profile
    sql_2 = "insert into kwippy_random_user(user_id,set_id,created_at) values("+str(profile[1])+","+str(set)+",now())"
    id = cur.execute(sql_2)
    print "inserted",id
    count += 1
cur.close()
conn.commit()
conn.close()