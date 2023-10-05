from django.contrib import admin
from .models import Review, Product, CustomUser#, Reviewer 

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    #list_display = ('rating', 'user_id', 'product_id', 'comment')
    list_display = ('review_id', 'product_name', 'rating', 'username', 'comment')
    search_fields = ('product_name__name', 'rating', 'username__username', 'comment')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'price', 'sold_count', 'seller', 'description', 'image')
    search_fields = ('name', 'price', 'sold_count')  # Add fields you want to search by



@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'gender', 'account', 'is_staff', 'is_active')

# @admin.register(Reviewer)
# class ReviewerAdmin(admin.ModelAdmin):
#     list_display = ('reviewer_id', 'username')