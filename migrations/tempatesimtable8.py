import sys, os, time

class tempatesimtable(object):
    def up(self,conn):
        # Write the migration here with comments
        print "up works"
        cursor = conn.cursor()
        cursor.execute("insert into kwippy_im(type,body) values('comment',%s)",('#_2 has left a comment on the kwip:<br>"#_3"<br><br>go read and reply here:<br>http://kwippy.com/#_4',))
        cursor.execute("insert into kwippy_im(type,body) values('follower',%s)",("you have got a new follower :)<br>#_1 so likes what you kwip that #_1's started following your kwips.<br><br>you could checkout #_1's page too:<br>http://kwippy.com/#_3",))
        cursor.execute("insert into kwippy_im(type,body) values('private_message',%s)",('#_2 has sent you a private message.<br><br>"#_3"<br><br>p.s. you can reply privately here - http://kwippy.com/#_4',))
        cursor.execute("insert into kwippy_im(type,body) values('buzz',%s)",('#_2 is missing your kwips, here is what #_2 has written:<br><br>"#_3"<br><br>p.s. you can check his profile out here - http://kwippy.com/#_4',))
        cursor.execute("insert into kwippy_im(type,body) values('comment_follower',%s)",('#_1 has left a comment on the kwip you are following:<br>"#_2"<br><br>go read and reply here:<br>http://kwippy.com/#_3',))
        cursor.execute("insert into kwippy_im(type,body) values('kwip',%s)",("""#_1 posted this:<br><br>#_2<br><br>go reply to this kwip here:<br>#_3""",))
        conn.commit()
    up = classmethod(up)    
    def down(self,conn):
        # Write reverting the migration here
        cursor = conn.cursor()
        cursor.execute("delete from kwippy_im where type like('comment','follower','private_message','buzz','comment_follower','kwip')")        
        print "down works"
        conn.commit()
    down = classmethod(down)    
