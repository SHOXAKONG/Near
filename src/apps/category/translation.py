from modeltranslation.translator import register, TranslationOptions
from .models import Category, Subcategory

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Subcategory)
class SubcategoryTranslationOptions(TranslationOptions):
    fields = ('name',)