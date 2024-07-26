# chat/forms.py
from django import forms
from .models import User

class LoginForm(forms.Form):
    nickname = forms.CharField(max_length=30)
