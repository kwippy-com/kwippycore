from django.db import models

# This is an object in the command queue
COMMAND_STATUS =((0, 'WAITING'), (1, 'RUNNING'),(2, 'SUCCESS'),(3, 'FAILED'))
MAIL_TYPE = ((1, 'NEW-COMMENT'), (2, 'NEW-FOLLOWER'),(3, 'PRIVATE-MESSAGE'),(4, 'BUZZ'))

class Commd(models.Model):
    type = models.IntegerField()
    obj_type = models.IntegerField(default=0)
    status = models.IntegerField(choices=COMMAND_STATUS,null = True)
    params = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    start_at = models.DateTimeField(null = True)
    end_at = models.DateTimeField(null = True)
    class Admin:
        pass
    
