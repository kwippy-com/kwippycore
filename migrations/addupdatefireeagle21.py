import sys, os, time

class addupdatefireeagle(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
	cursor.execute(" alter table `kwippy_user_profile` add column update_fire_eagle tinyint(1) NOT NULL")
        conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        cursor = conn.cursor()
        cursor.execute(" alter table kwippy_user_profile drop column update_fire_eagle")
        conn.commit()
    down = classmethod(down)    
