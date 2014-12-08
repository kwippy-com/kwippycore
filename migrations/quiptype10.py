import sys, os, time

class quiptype(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE `kwippy_quip` ADD column type integer NOT NULL")
	cursor.execute("UPDATE `kwippy_quip` SET type=0")
        conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        cursor = conn.cursor()
        cursor.execute("alter table kwippy_quip drop column type")
        conn.commit()
    down = classmethod(down)    
