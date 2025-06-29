from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Place

@admin.register(Place)
class PlaceAdmin(LeafletGeoAdmin):
    list_display = ('name', 'location')
