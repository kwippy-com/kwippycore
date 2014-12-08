import sys, os, time

class altercommentfollower(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
	cursor.execute("alter table kwippy_comment_follower add column is_active integer default 1;")
        conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        cursor = conn.cursor()
        cursor.execute(" alter table kwippy_comment_follower drop column is_active")
	conn.commit()
    down = classmethod(down)    
