import sys, os, time

class thumbnailversion(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
        cursor.execute("alter table kwippy_user_profile add `picture_ver` integer NOT NULL")
        conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        cursor = conn.cursor()
        cursor.execute("alter table kwippy_user_profile delete column `picture_ver`")
        conn.commit()
    down = classmethod(down)    
