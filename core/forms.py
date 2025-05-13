from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Album, Photo


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'is_private']

class PhotoForm(forms.ModelForm):
    # Fix A02 1/2: 
    #location = forms.CharField(required=False, max_length=255) # This creates a custom form field for location 

    class Meta:
        model = Photo
        # A02 : Cryptographic Failures - Encrypt location before saving
        fields = ['album', 'image', 'caption', 'location']  # Comment this line to fix A02

    # Fix A02 2/2: 
    #fields = ['album', 'image', 'caption'] # no location field in the form
    #def save(self, commit=True):
    #   photo = super().save(commit=False)
    #   location = self.cleaned_data.get('location')
    #
    #   if location:
    #       photo.location = location  # uses the @property setter to encrypt
    #
    #   if commit:
    #       photo.save() # overrode .save() to call "virtual location" setter
    #   return photo
