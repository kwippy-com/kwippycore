import sys, os, time

class populatenotificationsettings(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
        cursor.execute("alter table comm_queue_app_commd  ADD column mail_type varchar(25) NOT NULL")
        print int(cursor.execute("select * from auth_user where id not in (select user_id from kwippy_notificationsetting)"))
        user_ids = [int(item[0]) for item in cursor.fetchall()]
        for i in user_ids:
            sql_2 = "insert into kwippy_notificationsetting(user_id,email,im,updated_at) values(%d,'1,1,1,1,0','1,1,1,1,1',now())" % (i)                    
            cursor.execute(sql_2)            
            conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        conn.commit()
    down = classmethod(down)    
