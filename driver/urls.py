from django.conf.urls import url

from driver.views import DriverCreateView, DriverUpdateRetrieveDeleteView, DriverListView, DriverActiveAndLoadedListView, \
    DriverHasVehicleNumberRetrieveView, RegisterCreateView, RegisterUpdateRetrieveDeleteView, RegisterListView, \
    RegisterListByTruckView

app_name = 'driver'

urlpatterns = [
    url(r'register/create',
        RegisterCreateView.as_view({'post': 'create'}),
        name='register_create'),
    url(r'register/(?P<pk>\d+)/update_retrieve_delete',
        RegisterUpdateRetrieveDeleteView.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'}),
        name='register_update_retrieve_delete'),
    url(r'register/list',
        RegisterListView.as_view({'get': 'list'}),
        name='register_list'),
    url(r'register/loaded/list',
        RegisterListByTruckView.as_view({'post': 'list'}),
        name='register_loaded_list'),
    url(r'create',
        DriverCreateView.as_view({'post': 'create'}),
        name='driver_create'),
    url(r'(?P<pk>\d+)/update_retrieve_delete',
        DriverUpdateRetrieveDeleteView.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'}),
        name='driver_update_retrieve_delete'),
    url(r'list/hasVehicle',
        DriverHasVehicleNumberRetrieveView.as_view({'get': 'list'}),
        name='driver_has_vehicle_list'),
    url(r'list/unloaded',
        DriverActiveAndLoadedListView.as_view({'get': 'list'}),
        name='driver_active_unloaded_list'),
    url(r'list',
        DriverListView.as_view({'get': 'list'}),
        name='driver_list'),
]
