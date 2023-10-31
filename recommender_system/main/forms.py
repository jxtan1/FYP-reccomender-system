from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Review, CustomUser, Feedback

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required = True)
    #name = forms.CharField(max_length = 100)
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
    
    account_types = (
        ('', 'Select Account'),
        ('B', 'Buyer'),
        ('S', 'Seller')
    )
    account = forms.ChoiceField(
        choices = account_types,
        initial = '',
        widget = forms.Select(attrs={'class': 'custom-select'}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'gender', 'account', 'password1', 'password2']



class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'price', 'sold_count']


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            'rating',
            'easy_to_navigate',
            'additional_categories',
            'information_found',
            'comments',
        ]