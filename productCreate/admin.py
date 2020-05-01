from django.contrib import admin
from .models import Category, Products,ProductsImages,SubCategory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','price','slug',
    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(SubCategory)
admin.site.register(ProductsImages)