from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from .models import Album, Photo
from .forms import AlbumForm, PhotoForm, RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden
from django.db import connection


def home_redirect(request):
    return redirect('dashboard')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    albums = Album.objects.filter(owner=request.user)
    return render(request, 'dashboard.html', {'albums': albums})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def create_album(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        if form.is_valid():
            album = form.save(commit=False)
            album.owner = request.user
            album.save()
            return redirect('dashboard')
    else:
        form = AlbumForm()
    return render(request, 'create_album.html', {'form': form})

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        form.fields['album'].queryset = Album.objects.filter(owner=request.user)
        if form.is_valid():
            photo = form.save(commit=False) 
            photo.owner = request.user # Saving the owner of the photo
            photo.save()
            form.save()
            return redirect('dashboard')
    else:
        form = PhotoForm()
        form.fields['album'].queryset = Album.objects.filter(owner=request.user)
    return render(request, 'upload_photo.html', {'form': form})

@login_required
def view_album(request, album_id):
    album = get_object_or_404(Album, id=album_id)


    # A01: Broken Access Control: The users could access other users' "private" albums.
    
    #Uncomment the following code to reproduce the issue
    # How to test: login as one user, create an album, then log in as another and manually visit /albums/<AlbumID>/
    #photos = Photo.objects.filter(album=album)
    #return render(request, 'view_album.html', {
    #    'album': album,
    #    'photos': photos
    #})

    #A01:Broken Access Control -  Fix
    if album.owner != request.user and album.is_private: # Different owner or not a public album
        return HttpResponseForbidden("You are not allowed to access this album.")
    else:
        photos = Photo.objects.filter(album=album)
        return render(request, 'view_album.html', {
            'album': album,
            'photos': photos
        })

@login_required
def search_photos(request):
    query = request.GET.get('q', '')

    # A03: SQL Injection: The search query is allowing SQL injection attacks
    # Uncomment the following code to reproduce the issue
    # How to test: Search in the app:   ?q=' OR 1=1--  
     
    #raw_query = f"""
    #   SELECT * FROM core_photo
    #   WHERE owner_id = {request.user.id} AND
    #   caption LIKE '%{query}%'
    #"""
    #with connection.cursor() as cursor:
    #   cursor.execute(raw_query)
    #   photos = cursor.fetchall()
    #
    #return render(request, 'search_results.html', {
    #   'photos': photos,
    #   'query': query
    #})

    # A03: SQL Injection - Fix
    query = request.GET.get('q', '')
    photos = Photo.objects.filter(caption__icontains=query, album__owner=request.user) # ORM automatically parameterizes input
    print(photos)
    return render(request, 'search_results.html', {
        'photos': photos,
        'query': query
    })