from django.db import models

from django.contrib.auth.models import User

class Room(models.Model):
    name      = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Message(models.Model):
    name      = models.ForeignKey(User, on_delete=models.CASCADE)
    room      = models.ForeignKey(Room, on_delete=models.CASCADE)
    text      = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('timestamp',)

    def __str__(self):
        return self.text