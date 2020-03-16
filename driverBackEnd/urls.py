"""driverBackEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="driverBackEnd - API",
      default_version='Beta',
      description="REST API for driverBackEnd.",
      contact=openapi.Contact(email="unlisislukasferreira@hotmail.com"),
      license=openapi.License(name="Public"),
   ),
   public=True,
   permission_classes=(permissions.IsAdminUser,),
)

doc_urls = [
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/driver/', include('driver.urls', namespace='driver')),
    url(r'^api/order/', include('order.urls', namespace='order')),
    url(r'^api/location/', include('location.urls', namespace='location')),
    url(r'^api/truck/', include('truck.urls', namespace='truck')),
] + doc_urls
