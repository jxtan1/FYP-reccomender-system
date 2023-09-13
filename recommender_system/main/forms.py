from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Review

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required = True)
    name = forms.CharField(max_length = 100)
    gender_choices = (
        ('', 'Select Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = forms.ChoiceField(
        choices = gender_choices,
        initial ='',  # Initially, no selection (placeholder)
        widget = forms.Select(attrs={'class': 'custom-select'}),
    )  

    class Meta:
        model = User
        fields = ['username', 'name', 'gender', 'email', 'password1', 'password2']



class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description']