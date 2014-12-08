import sys, os, time

class userprofilecount(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
	cursor.execute(" alter table `kwippy_user_profile` add column `quip_total` integer NULL")
        cursor.execute(" alter table `kwippy_user_profile` add column `quip_repeat_total` integer NULL")
        cursor.execute(" alter table `kwippy_user_profile` add column `comment_count` integer NULL")
        cursor.execute(" alter table `kwippy_user_profile` add column `fav_count` integer NULL") 
        cursor.execute(" update kwippy_user_profile set quip_repeat_total=(select count(*) from kwippy_quip where kwippy_user_profile.user_id=kwippy_quip.user_id)")
        cursor.execute(" update kwippy_user_profile set quip_total=(select count(*) from kwippy_quip where repeat_id in (0,id) and kwippy_user_profile.user_id=kwippy_quip.user_id)")
        cursor.execute(" update kwippy_user_profile set comment_count=(select count(*) from comments_comment where content_type_id=19 and comments_comment.user_id=kwippy_user_profile.user_id)")
        cursor.execute(" update kwippy_user_profile set fav_count=(select count(*) from kwippy_favourite where kwippy_favourite.user_id=kwippy_user_profile.user_id)")
    	conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        print "down works"
        cursor = conn.cursor()
        cursor.execute(" alter table kwippy_user_profile drop column quip_total")
        cursor.execute(" alter table kwippy_user_profile drop column quip_repeat_total")
        cursor.execute(" alter table kwippy_user_profile drop column comment_count")
        cursor.execute(" alter table kwippy_user_profile drop column fav_count")
	conn.commit()
    down = classmethod(down)    
