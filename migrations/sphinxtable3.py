import sys, os, time

class sphinxtable(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
        cursor.execute("create table sph_counter( id INT NOT NULL PRIMARY KEY, max_id INT)")
        conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        cursor = conn.cursor()
        cursor.execute("drop table sph_counter")
        conn.commit()
    down = classmethod(down)    
