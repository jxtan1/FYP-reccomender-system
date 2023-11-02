from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('home', views.home, name = 'home'),
    path('sign-up', views.sign_up, name = 'sign_up'),
    path('add-product', views.add_product, name = 'add_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('import/', views.import_from_excel, name='import_from_excel'),
    path('search/', views.search_products, name='search_products'),
    
    
    path('edit_account/', views.edit_account, name='edit_account'),
    path('view_account/', views.view_account, name='view_account'),
    path('change_password',views.change_password,name='change_password'),
    path('password_change_done',views.PasswordChangeDoneView.as_view(), name= 'password_change_done'),  
    path('delete_account',views.delete_account, name = 'delete_account'),  

    
    
    
]




