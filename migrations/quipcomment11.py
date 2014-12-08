import sys, os, time

class quipcomment(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
	cursor.execute("ALTER TABLE `kwippy_quip` ADD `last_comment_at` datetime NULL")
    	cursor.execute("ALTER TABLE `kwippy_quip` ADD `comment_count` integer NOT NULL")
    	cursor.execute("ALTER TABLE `kwippy_quip` ADD `last_comment_id` integer NULL")
	cursor.execute("UPDATE `kwippy_quip` SET comment_count=0")
        conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        cursor = conn.cursor()
        cursor.execute("alter table kwippy_quip drop column last_comment_at")
	cursor.execute("alter table kwippy_quip drop column last_comment_id")
	cursor.execute("alter table kwippy_quip drop column comment_count")
        conn.commit()
    down = classmethod(down)    
