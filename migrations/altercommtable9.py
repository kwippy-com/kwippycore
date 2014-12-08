import sys, os, time

class altercommtable(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
        cursor.execute("alter table comm_queue_app_commd ADD obj_type integer default 0 NOT NULL")
        conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        cursor = conn.cursor()
        cursor.execute("alter table comm_queue_app_commd drop column obj_type")        
        print "down works"
        conn.commit()
    down = classmethod(down)    
