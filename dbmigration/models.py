from django.db import models

# Contains the migration history
class MigrationHistory(models.Model):
    migration = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
