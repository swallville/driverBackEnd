from django.contrib import admin

# Register your models here.
from order.models import Order

admin.site.register(Order)

admin.site.site_title = 'Driver - Administration'
admin.site.site_header = 'Driver - Administration'
