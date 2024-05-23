# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from asset_management import views as asset_views

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', asset_views.register, name='register'),
    path('', redirect_to_login),
    path('assets/', include('asset_management.urls')),
]
