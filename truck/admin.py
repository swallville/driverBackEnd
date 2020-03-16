from django.contrib import admin

# Register your models here.
from truck.models import Truck

admin.site.register(Truck)

admin.site.site_title = 'Driver - Administration'
admin.site.site_header = 'Driver - Administration'
