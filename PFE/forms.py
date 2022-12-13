from django.contrib.auth.models import User
from django import forms

class SignUpForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    email=forms.EmailField(max_length=254,help_text='Obligatoire')
    class Meta:
        model=User
        fields=["username","email","password"]

class SignInForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=["username","password"]