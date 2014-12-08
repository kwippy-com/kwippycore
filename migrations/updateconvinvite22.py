import sys, os, time

class updateconvinvite(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
	cursor.execute(" alter table `kwippy_conversationinvite` add column comment_count tinyint(1) NOT NULL")
        conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        cursor = conn.cursor()
        cursor.execute(" alter table `kwippy_conversationinvite` drop column comment_count")
        conn.commit()
    down = classmethod(down)    
