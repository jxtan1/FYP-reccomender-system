from django.shortcuts import render, redirect
from .forms import RegisterForm, ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Product, Review

# Create your views here.
# In views.py
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_authenticated and user.is_staff  # Check if the user is authenticated and is a staff member (admin).

@login_required(login_url="/login")
def home(request):
    products = Product.objects.all()
    return render(request, 'main/home.html', {"products": products})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})

@login_required(login_url="/login")
@user_passes_test(is_admin, login_url="/home")
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            #product.productId = ProductForm.
            product.save()
            return redirect('/home')
    else:
        form = ProductForm()

    return render(request, 'main/add_product.html', {"form": form})

