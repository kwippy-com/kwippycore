import sys, os, time

class repeat(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE `kwippy_quip` ADD column repeat_id integer NOT NULL")
        cursor.execute("ALTER TABLE `kwippy_quip` ADD CONSTRAINT repeat_id_refs_id_62a4e99b FOREIGN KEY (`repeat_id`) REFERENCES `kwippy_quip` (`id`)")
	cursor.execute("INSERT INTO kwippy_filtercount(fid,count) VALUES(0,0)")
	cursor.execute 
        conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        cursor = conn.cursor()
        cursor.execute("alter table kwippy_quip drop column repeat_id")
        conn.commit()
    down = classmethod(down)    
