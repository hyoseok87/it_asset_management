# asset_management/forms.py
from django import forms
from .models import Asset

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'asset_type', 'location', 'purchase_date', 'price']
