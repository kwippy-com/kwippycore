import sys, os, time

class alteruserprofile(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
	cursor.execute(" alter table kwippy_user_profile add column theme_id integer null")
    	conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        cursor = conn.cursor()
        cursor.execute(" alter table kwippy_user_profile drop column theme_id")
	conn.commit()
    down = classmethod(down)    
