# asset_management/admin.py
from django.contrib import admin
from .models import Asset, MaintenanceRecord, License

admin.site.register(Asset)
admin.site.register(MaintenanceRecord)
admin.site.register(License)
