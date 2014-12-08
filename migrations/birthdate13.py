import sys, os, time

class birthdate(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
	cursor.execute("ALTER TABLE kwippy_user_profile ADD birth_day int NULL")
        cursor.execute("ALTER TABLE kwippy_user_profile ADD birth_month int NULL")
        cursor.execute("ALTER TABLE kwippy_user_profile ADD birth_year int NULL")
    	conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        cursor = conn.cursor()
        cursor.execute("alter table kwippy_user_profile drop birth_day")
        cursor.execute("alter table kwippy_user_profile drop birth_month")
        cursor.execute("alter table kwippy_user_profile drop birth_year")
	conn.commit()
    down = classmethod(down)    
