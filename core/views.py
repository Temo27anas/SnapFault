from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from .models import Album, Photo
from .forms import AlbumForm, PhotoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

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
            form.save()
            return redirect('dashboard')
    else:
        form = PhotoForm()
        form.fields['album'].queryset = Album.objects.filter(owner=request.user)
    return render(request, 'upload_photo.html', {'form': form})
