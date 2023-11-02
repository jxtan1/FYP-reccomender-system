from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, ProductForm, UserProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Product, Reviewer, Review
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User

# Create your views here.
# In views.py
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_authenticated and user.is_staff  # Check if the user is authenticated and is a staff member (admin).

@login_required(login_url="/login")
def home(request):
    all_products = Product.objects.order_by('product_id')
    # Create a Paginator object with a specified number of products per page
    paginator = Paginator(all_products, 50)  # Change 50 to the number of products per page you desire

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    # Get the products for the current page
    products = paginator.get_page(page)
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


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product_name=product)
    
    # Create a Paginator object for reviews
    paginator = Paginator(reviews, 10)  # Change 10 to the number of reviews per page you desire

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    # Get the Page object for the current page of reviews
    reviews = paginator.get_page(page)

    context = {
        'product': product,
        'reviews': reviews,
    }
    return render(request, 'main/product_detail.html', context)


def search_products(request):
    query = request.GET.get('q')
    
    # Filter products based on the search query
    products = Product.objects.filter(Q(name__icontains=query)).order_by('name')
    
    # Create a Paginator object
    paginator = Paginator(products, 50)  # Change 50 to the number of products per page you desire

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page')

    # Get the Page object for the current page
    products = paginator.get_page(page)

    return render(request, 'main/home.html', {"products": products})



@login_required
def view_account(request):
    user = request.user  # Retrieve the current user
    return render(request, 'main/view_account.html', {'user': user})

@login_required
def edit_account(request):
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/view_account')
    else:
        form = UserProfileEditForm(instance=request.user)
    return render(request, 'main/edit_account.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to prevent the user from being logged out
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/view_account')
        else:
            messages.error(request, 'Please correct the error(s) below.')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'registration/change_password.html', {'form': form})

class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('password_change_done')  # Redirect to a success page after changing the password

class PasswordChangeDoneView(TemplateView):
    template_name = 'registration/password_change_done.html'

    @login_required
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@login_required
def delete_account(request):
    if request.method == 'POST' and 'confirm_delete' in request.POST:
        # Delete the user account
        user = request.user
        user.delete()

        return redirect('logout')  # You can redirect to the logout view or any other appropriate page
    return render(request, 'main/confirm_delete.html')



from openpyxl import load_workbook
import pandas as pd
from django.db import IntegrityError

@login_required(login_url="/login")
@user_passes_test(is_admin, login_url="/home")
def import_from_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        
        
        # wb = load_workbook(excel_file)
        # ws = wb.active
        
        # for row in ws.iter_rows(min_row=2, values_only=True):
        #     name, price, sold_count = row
        #     Product.objects.create(name=name, price=price, sold_count=sold_count)
        
        # Convert to pandas dataframe
        df = pd.read_excel(excel_file)
        df.drop_duplicates() # Cleaning
        
        # Handle Product data
        if request.POST.get('import_type') == "Product":
            df.pop(df.columns[-1]) # Remove urls from dataset
            # Rename columns to match model
            rename_columns = {"Product Name": "name", "Price": "price", "Total Sold": "sold_count"}
            df.rename(columns = rename_columns, inplace=True)
            df['sold_count'] = df['sold_count'].str.replace(',', '').astype(int) # Change sold_count to int
            data = df.to_dict('records') # Convert dataframe into dictionaries
            # Loop over list of dictionaries and save each one to the Product model
            for item in data:
                try:
                    product = Product.objects.update_or_create(**item)
                    product[0].save()
                except IntegrityError as e:
                    if 'unique constraint' in e.args[0]:
                        #Skip repeats
                        print(e)
        
        # Handle Review data
        elif request.POST.get('import_type') == "Review":
            df.pop('Date') # Remove dates from dataset
            # Rename columns to match review model
            rename_columns = {"Product Name": "product_name", "Rating": "rating", "Reviewer": "username", "Content": "comment"}
            df.rename(columns = rename_columns, inplace=True)
            reviewers = (((df.loc[:,'username']).drop_duplicates()))#.rename(columns = {"Reviewer": "username"})).to_dict() # Get unique reviewers
            # Save all reviewers from the reviews gathered to the Reviewer model
            for item in reviewers:
                # Need a way to catch verify unique=True error
                try:
                    reviewer = Reviewer(username=item) # Should not update any existing due to unique constraint
                    reviewer.save()
                except IntegrityError as e:
                    if 'unique constraint' in e.args[0]:
                        #Skip repeats
                        print(e)
            data = df.to_dict('records') # Convert dataframe into dictionaries
            # Loop over list of dictionaries and save each one to the Product model
            for item in data:
                # Find product & reviewer objects
                #product = Product.objects.filter(name=item["product_name"])
                #product = get_object_or_404(Product, name=item["product_name"])
                try:
                    product = Product.objects.get(name=item["product_name"])
                except Product.DoesNotExist:
                    # Skip products not in database
                    print(item["product_name"], "not found!")
                    continue
                #reviewer = Reviewer.objects.filter(username=item["username"])
                reviewer = get_object_or_404(Reviewer, username=item["username"])
                #review = Review(**item)
                review = Review.objects.update_or_create(product_name=product, rating=item["rating"], username=reviewer, comment=item["comment"])
                review[0].save()
        
        return render(request, 'main/import_success.html')
    return render(request, 'main/import_form.html')
        
