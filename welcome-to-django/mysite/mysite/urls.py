from django.contrib import admin
from django.urls import path, include

from register import views as register_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_views.register, name='register'),
    path('', include('main.urls')),
    path('', include('django.contrib.auth.urls')),
]