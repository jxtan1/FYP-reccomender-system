from django.urls import path
from django.contrib import admin
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
    path('customer_feedback/', views.customer_feedback_view, name='customer_feedback_form'),
    path('seller_feedback/', views.seller_feedback_view, name='seller_feedback_form'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('view_account/', views.view_account, name='view_account'),
    path('change_password',views.change_password,name='change_password'),
    path('password_change_done',views.PasswordChangeDoneView.as_view(), name= 'password_change_done'),  
    path('delete_account',views.delete_account, name = 'delete_account'),  
    path('seller/my_products', views.SellerProductListView.as_view(), name='seller_products'),
    path('seller/my_products/<int:product_id>/edit/', views.edit_product, name='edit_product'),
    path('seller/my_products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path('seller/<str:username>/store/', views.seller_store, name='seller_store'),

   ####
   
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),

    path('cart/', views.cart_view, name='cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
]


#admin.site.index_title = 'E-commerce Website'
admin.site.site_header = 'Blue Moon'
admin.site.site_title = 'Admin Dashboard'
    





