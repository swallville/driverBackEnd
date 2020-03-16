from django.contrib.admin import AdminSite
from django.contrib import admin


class CustomAdmin(AdminSite):
    index_template = 'admin/base_site.html'


admin.register(CustomAdmin)