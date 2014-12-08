import sys, os, time

class alterpagesettings(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE `kwippy_pagesetting` ADD CONSTRAINT user_id_refs_id_541e14b3e5aeb03c FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)")
	cursor.execute("CREATE UNIQUE INDEX `kwippy_pagesetting_user_id` ON `kwippy_pagesetting` (`user_id`)")
	cursor.execute 
        conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        conn.commit()
    down = classmethod(down)    
