from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

# Register your models here.
from location.models import Location


@admin.register(Location)
class LocationAdmin(OSMGeoAdmin):
    list_display = ('address', 'city', 'zip_code', 'location')
