from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import CustomUser, Product, Review#, Reviewer 
from django.core.paginator import Paginator
from django.db.models import Q


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


from openpyxl import load_workbook
import pandas as pd
from django.db import IntegrityError

@login_required(login_url="/login")
@user_passes_test(is_admin, login_url="/home")
def import_from_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']

        # Read file and convert to pandas dataframe
        df = pd.read_excel(excel_file)
        df.drop_duplicates() # Cleaning
        
        # Handle Product data
        if request.POST.get('import_type') == "Product":
            #df.pop(df.columns[-1]) # Remove urls from dataset
            df.pop('Product Page')
            # Rename columns to match model
            rename_columns = {"Product Name": "name", "Price": "price", "Total Sold": "sold_count", "Seller": 'seller', "Description": "description", "Image": "image"}
            df.rename(columns = rename_columns, inplace=True)
            df['sold_count'] = df['sold_count'].str.replace(',', '').astype(int) # Change sold_count to int
            sellers = (df.loc[:,'seller']).drop_duplicates() # Get unique sellers
            # Save all sellers from products gathered to the Seller model
            for item in sellers:
                # Need a way to catch verify unique=True error
                try:
                    seller = CustomUser(username=item, account='S') # Should not update any existing due to unique constraint
                    seller.save()
                except IntegrityError as e:
                    if 'unique constraint' in e.args[0]:
                        #Skip repeats
                        print(e)
            data = df.to_dict('records') # Convert dataframe into dictionaries
            # Loop over list of dictionaries and save each one to the Product model
            for item in data:
                try:
                    seller = CustomUser.objects.get(username=item['seller'], account='S')
                except CustomUser.DoesNotExist:
                    # Skip sellers not in the database
                    print(item[''], "not found!")
                    continue
                try:
                    product = Product.objects.update_or_create(name=item['name'], price=item['price'], sold_count=item['sold_count'], seller=seller, description=item['description'], image=item['image'])
                    product[0].save()
                except IntegrityError as e:
                    if 'unique constraint' in e.args[0]:
                        # Skip repeats
                        print('Duplicate', item['name'], 'found, ignoring...')
        
        # Handle Review data
        elif request.POST.get('import_type') == "Review":
            # Rename columns to match review model
            rename_columns = {"Product Name": "product_name", "Rating": "rating", "Reviewer": "username", "Content": "comment"}
            df.rename(columns = rename_columns, inplace=True)
            reviewers = (df.loc[:,'username']).drop_duplicates() # Get unique reviewers
            # Save all reviewers from the reviews gathered to the seller (CustomUser account='B') model
            for item in reviewers:
                # Need a way to catch verify unique=True error
                try:
                    reviewer = CustomUser(username=item, account='B') # Should not update any existing due to unique constraint
                    reviewer.save()
                except IntegrityError as e:
                    if 'unique constraint' in e.args[0]:
                        # Skip repeats
                        print(e)
            data = df.to_dict('records') # Convert dataframe into dictionaries
            # Loop over list of dictionaries and save each one to the Product model
            for item in data:
                # Find product & seller (CustomUser Account='B') objects
                try:
                    product = Product.objects.get(name=item["product_name"])
                except Product.DoesNotExist:
                    # Skip products not in database
                    print(item["product_name"], "not found!")
                    continue
                try:
                    reviewer = CustomUser.objects.get(username=item["username"], account='B')
                except CustomUser.DoesNotExist:
                    # Skip if cannot find reviewer
                    continue
                review = Review.objects.update_or_create(product_name=product, rating=item["rating"], username=reviewer, comment=item["comment"])
                review[0].save()
        
        return render(request, 'main/import_success.html')
    return render(request, 'main/import_form.html')
        
