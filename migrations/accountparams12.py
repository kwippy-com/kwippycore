import sys, os, time

class accountparams(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
	cursor.execute("ALTER TABLE `kwippy_account` ADD `other_param` varchar(200) NOT NULL")
        conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        cursor = conn.cursor()
        cursor.execute("alter table kwippy_account drop column other_param")
        conn.commit()
    down = classmethod(down)    
