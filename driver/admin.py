from django.contrib import admin

# Register your models here.
from driver.models import Driver, Register

admin.site.register(Driver)
admin.site.register(Register)

admin.site.site_title = 'Driver - Administration'
admin.site.site_header = 'Driver - Administration'
