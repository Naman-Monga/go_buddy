from django.db import models

# Create your models here.
class Room(models.Model):
    admin = models.IntegerField()
    room_name = models.CharField(max_length=1000)
    room_title = models.CharField(max_length=1000, null=True, blank=True)
    def __str__(self) -> str:
        return self.room_name