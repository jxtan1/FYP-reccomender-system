from django.shortcuts import render, redirect
from .forms import RegisterForm, ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Product, Reviewer, Review

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


from django.shortcuts import render, get_object_or_404
from .models import Product, Review

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product_name=product)
    context = {
        'product': product,
        'reviews': reviews,
    }
    return render(request, 'main/product_detail.html', context)

from openpyxl import load_workbook
import pandas as pd
from django.db import IntegrityError

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
                    product = Product(**item)
                    product.save()
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
                    reviewer = Reviewer(username=item)
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
                product = get_object_or_404(Product, name=item["product_name"])
                #reviewer = Reviewer.objects.filter(username=item["username"])
                reviewer = get_object_or_404(Reviewer, username=item["username"])
                #review = Review(**item)
                review = Review(product_name=product, rating=item["rating"], username=reviewer, comment=item["comment"])
                review.save()
        
        return render(request, 'main/import_success.html')
    return render(request, 'main/import_form.html')
        
