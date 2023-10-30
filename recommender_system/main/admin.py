from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from .models import Review, Product, CustomUser#, Reviewer 

# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    #list_display = ('rating', 'user_id', 'product_id', 'comment')
    list_display = ('review_id', 'product_name', 'rating', 'username', 'comment')
    search_fields = ('product_name__name', 'rating', 'username__username', 'comment')
    list_filter = ('rating',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'price', 'sold_count', 'seller', 'description', 'image')
    search_fields = ('name', 'price', 'sold_count')  # Add fields you want to search by

class EmailFilter(admin.SimpleListFilter):
    title  = 'Email Filter'
    parameter_name = 'user_email'

    def lookups(self, request, model_admin):
        return (
            ('has_email', 'has email'),
            ('no_email', 'no email')
        )
    
    def queryset(self, request, queryset) :
        if not self.value():
            return queryset
        if self.value().lower() == 'has_email':
            return queryset.exclude(email='')
        if self.value().lower() == 'no_email':
            return queryset.filter(email='')


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):

    fieldsets = (
        ('User Account Credentials', {
            'fields': ('username', 'password',),
            'description': 'Fields needed for login',
        }),
        ('User Info', {
            'fields': ('first_name', 'last_name', 'gender', 'email'),
            'description': 'Personal info of users like name, gender, etc.',
        }),
        ('User Account Info', {
            'fields': ('account','is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login'),
            'description': 'Default user account info fields',
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'gender', 'account', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')  # Add fields you want to search by
    list_filter = ("is_active", 'account', 'is_staff', 'gender', 'date_joined', EmailFilter)

# @admin.register(Reviewer)
# class ReviewerAdmin(admin.ModelAdmin):
#     list_display = ('reviewer_id', 'username')

