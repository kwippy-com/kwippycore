import sys, os, time

class alterquip(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
	cursor.execute(" alter table kwippy_quip add column `user_id` integer NULL")
        cursor.execute(" update kwippy_quip set user_id=(select user_id from kwippy_account where kwippy_account.id=kwippy_quip.account_id) ")
        cursor.execute("CREATE INDEX `kwippy_quip_user_id` ON `kwippy_quip` (`user_id`)")
        cursor.execute("CREATE INDEX `kwippy_quip_repeat_id` ON `kwippy_quip` (`repeat_id`)")
        cursor.execute("CREATE INDEX `kwippy_quip_last_comment_id` ON `kwippy_quip` (`last_comment_id`)")
        cursor.execute("CREATE INDEX `kwippy_user_profile_country_id` ON `kwippy_user_profile` (`country_id`)")
        cursor.execute("CREATE INDEX `kwippy_user_profile_theme_id` ON `kwippy_user_profile` (`theme_id`)")
    	conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        cursor = conn.cursor()
        cursor.execute(" alter table kwippy_quip drop column user_id")
	conn.commit()
    down = classmethod(down)    
