# asset_management/forms.py
from django import forms
from .models import Asset
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'asset_type', 'location', 'purchase_date', 'price']

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
