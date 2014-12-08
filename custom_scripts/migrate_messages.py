import urllib, urllib2, MySQLdb
site = 'http://localhost:1000'

conn = MySQLdb.connect(host='localhost',user='root',passwd='mayank',db='kwippy_staging')
cur = conn.cursor()
sql_1 = "select * from kwippy_private_message where id not in (select pm_id from kwippy_list_filter)"
no_of_pms = int(cur.execute(sql_1))
print no_of_pms
rows=cur.fetchall()
for row in rows:    
    sql_2 = "insert into kwippy_list_filter(receiver_user_id,pm_id,status,created_at) values("+str(row[2])+","+str(row[0])+", 0,"+"'"+str(row[5].strftime("%Y-%m-%d"))+"'"+")"    
    cur.execute(sql_2)
    sql_3 = "insert into kwippy_sent_filter(sender_user_id,pm_id,created_at) values("+str(row[1])+","+str(row[0])+","+"'"+str(row[5].strftime("%Y-%m-%d"))+"'"+")"
    cur.execute(sql_3)    
cur.close()
conn.commit()
conn.close()
    
