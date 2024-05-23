# asset_management/models.py
from django.db import models

class Asset(models.Model):
    name = models.CharField(max_length=100)
    ASSET_TYPE_CHOICES = [
        ('laptop', 'Laptop'),
        ('desktop', 'Desktop'),
        ('server', 'Server'),
        ('network', 'Network Equipment'),
        ('windows', 'License'),
        ('monitor', 'Monitor'),
        ('drucker', 'Drucker')
    ]
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPE_CHOICES)
    location = models.CharField(max_length=100)
    purchase_date = models.DateField()
    price = models.FloatField()

    def __str__(self):
        return self.name

class MaintenanceRecord(models.Model):
    asset = models.ForeignKey(Asset, related_name='maintenance_records', on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.asset.name} - {self.date}"

class License(models.Model):
    asset = models.ForeignKey(Asset, related_name='licenses', on_delete=models.CASCADE)
    software_name = models.CharField(max_length=100)
    license_key = models.CharField(max_length=100)
    expiry_date = models.DateField()

    def __str__(self):
        return self.software_name



