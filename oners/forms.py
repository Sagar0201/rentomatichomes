from django import forms
from django.contrib.auth.models import User
from django.db.models import fields
from .models import Profile


class UserUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class ProfileUpdate(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
