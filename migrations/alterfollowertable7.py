import sys, os, time

class alterfollowertable(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
        cursor.execute("alter table kwippy_follower  ADD column im_notification tinyint(1) default 0 NOT NULL")
        conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        cursor = conn.cursor()
        cursor.execute("alter table kwippy_follower  drop column im_notification")        
        print "down works"
        conn.commit()
    down = classmethod(down)    
