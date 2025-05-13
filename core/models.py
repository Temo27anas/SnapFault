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
    # A02 – Cryptographic Failures: Exposed location field
    location = models.TextField(max_length=255, blank=True) # Comment this line to fix A02
    
    #Fix A02 : The model exposes location as a virtual property handling encryption/decryption
    #encrypted_location = models.TextField(blank=True)
    #@property
    #def location(self):
    #   if self.encrypted_location:
    #       return decrypt_location(self.encrypted_location)
    #   return ''
    #
    #@location.setter
    #def location(self, value):
    #   if value:
    #       self.encrypted_location = encrypt_location(value)
