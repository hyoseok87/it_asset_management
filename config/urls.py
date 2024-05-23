# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from asset_management import views as asset_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', asset_views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('assets/', asset_views.asset_list, name='asset_list'),
    path('asset/<int:asset_id>/', asset_views.asset_detail, name='asset_detail'),
    path('asset/create/', asset_views.asset_create, name='asset_create'),
    path('asset/edit/<int:asset_id>/', asset_views.asset_edit, name='asset_edit'),
    path('asset/delete/<int:asset_id>/', asset_views.asset_delete, name='asset_delete'),
    path('export_assets_csv/', asset_views.export_assets_csv, name='export_assets_csv'),
    path('import_assets_csv/', asset_views.import_assets_csv, name='import_assets_csv'),
    path('', RedirectView.as_view(url='/accounts/login/')),
]
