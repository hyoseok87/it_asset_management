# asset_management/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('assets/', views.asset_list, name='asset_list'),
    path('assets/<int:asset_id>/', views.asset_detail, name='asset_detail'),
    path('assets/new/', views.asset_create, name='asset_create'),
    path('assets/<int:asset_id>/edit/', views.asset_edit, name='asset_edit'),
    path('assets/<int:asset_id>/delete/', views.asset_delete, name='asset_delete'),
]
