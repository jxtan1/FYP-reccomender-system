from django.contrib import admin
from .models import Review, Product, CustomUser 

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    #list_display = ('rating', 'user_id', 'product_id', 'comment')
    list_display = ('rating', 'user_id', 'product_id', 'comment')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'product_owner', 'description')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'gender', 'is_staff', 'is_active')

