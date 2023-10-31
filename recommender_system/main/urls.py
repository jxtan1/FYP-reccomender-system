from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('home', views.home, name = 'home'),
    path('sign-up', views.sign_up, name = 'sign_up'),
    path('add-product', views.add_product, name = 'add_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('import/', views.import_from_excel, name='import_from_excel'),
    path('search/', views.search_products, name='search_products'),
    path('feedback/', views.feedback_view, name='feedback_form'),

]


#admin.site.index_title = 'E-commerce Website'
admin.site.site_header = 'E-commerce Website Admin Area'
admin.site.site_title = 'Admin Dashboard'