from django.conf.urls import url

from truck.views import TruckCreateView, TruckUpdateRetrieveDeleteView, TruckListView

app_name = 'truck'

urlpatterns = [
    url(r'(?P<pk>\d+)/update_retrieve_delete',
        TruckUpdateRetrieveDeleteView.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'}),
        name='truck_update_retrieve_delete'),
    url(r'create',
        TruckCreateView.as_view({'post': 'create'}),
        name='truck_create'),
    url(r'list',
        TruckListView.as_view({'get': 'list'}),
        name='truck_list'),
]
