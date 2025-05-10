from django.db import models
from django.contrib.auth.models import User

class Album(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE) # CASCADE: if the user is deleted, all their albums are also deleted
    name = models.CharField(max_length=255)
    is_private = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Photo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE) 
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/')
    caption = models.TextField(blank=True) 


    def __str__(self):
        return f"{self.album.name} - {self.caption[:20]}"