import sys, os, time

class country(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
	cursor.execute("ALTER TABLE kwippy_user_profile ADD country_id varchar(3) NULL")
    	conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        cursor = conn.cursor()
        cursor.execute("alter table kwippy_user_profile drop country_id")
	conn.commit()
    down = classmethod(down)    
