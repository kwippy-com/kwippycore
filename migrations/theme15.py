import sys, os, time

class theme(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
	cursor.execute("alter table kwippy_pagesetting add theme_type int(1) NOT NULL")
    	conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        cursor = conn.cursor()
        cursor.execute("alter table kwippy_pagesetting drop theme_type")
	conn.commit()
    down = classmethod(down)    
