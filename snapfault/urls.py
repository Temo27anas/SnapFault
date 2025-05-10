from django.contrib import admin
from django.urls import path
from core import views as core_views
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', core_views.home_redirect, name='home'),
    path('admin/', admin.site.urls),
    path('register/', core_views.register_view, name='register'),
    path('dashboard/', core_views.dashboard, name='dashboard'),
    path('login/', core_views.login_view, name='login'),
    path('logout/', core_views.logout_view, name='logout'),
    path('albums/new/', core_views.create_album, name='create_album'),
    path('photos/upload/', core_views.upload_photo, name='upload_photo'),
    path('albums/<int:album_id>/', core_views.view_album, name='view_album'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

