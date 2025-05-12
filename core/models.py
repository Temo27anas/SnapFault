from django.db import models
from django.contrib.auth.models import User
from .encryption import encrypt_location, decrypt_location



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
    # A02 – Cryptographic Failures: 
    # The form saves the location in an exposed way. (Originally, it was saved in plaintext.)
    location = models.CharField(max_length=255, blank=True)
