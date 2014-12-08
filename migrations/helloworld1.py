import sys, os, time

class helloworld(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
        cursor.execute("select * from kwippy_quip")
        conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        cursor = conn.cursor()
        cursor.execute("select * from comm_queue_app_commd")
        conn.commit()
    down = classmethod(down)    
