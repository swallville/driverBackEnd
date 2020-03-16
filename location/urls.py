from django.conf.urls import url

from location.views import LocationCreateView, LocationUpdateRetrieveDeleteView, LocationListView

app_name = 'location'

urlpatterns = [
    url(r'create',
        LocationCreateView.as_view({'post': 'create'}),
        name='location_create'),
    url(r'(?P<pk>\d+)/update_retrieve_delete',
        LocationUpdateRetrieveDeleteView.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'}),
        name='location_update_retrieve_delete'),
    url(r'list',
        LocationListView.as_view({'get': 'list'}),
        name='location_list'),
]
