from django.contrib import admin
from .models import Category, Subcategory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    pass