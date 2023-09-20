from django.contrib import admin
from .models import Review, Product, CustomUser, Reviewer 

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    #list_display = ('rating', 'user_id', 'product_id', 'comment')
    list_display = ('product_name', 'rating', 'username', 'comment')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'price', 'sold_count')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'gender', 'is_staff', 'is_active')

@admin.register(Reviewer)
class ReviewerAdmin(admin.ModelAdmin):
    list_display = ('reviewer_id', 'username')