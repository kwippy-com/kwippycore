import sys, os, time

class alterprivatemessage(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
	cursor.execute(" alter table kwippy_private_message change message message longtext NOT NULL;")
    	conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        cursor = conn.cursor()
        cursor.execute(" alter table kwippy_private_message change message message varchar(500) not null;")
	conn.commit()
    down = classmethod(down)    
