from modeltranslation.translator import register, TranslationOptions
from .models import Place

@register(Place)
class PlaceTranslationOptions(TranslationOptions):
    fields = ('name',)