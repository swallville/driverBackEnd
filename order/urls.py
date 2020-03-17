from django.conf.urls import url

from order.views import OrderCreateView, OrderUpdateRetrieveDeleteView, OrderListView, OrderListByDriverView, OrderListByTruckView

app_name = 'order'

urlpatterns = [
    url(r'create',
        OrderCreateView.as_view({'post': 'create'}),
        name='order_create'),
    url(r'(?P<pk>\d+)/update_retrieve_delete',
        OrderUpdateRetrieveDeleteView.as_view({'put': 'update', 'get': 'retrieve', 'delete': 'destroy'}),
        name='order_update_retrieve_delete'),
    url(r'list/byDriver',
        OrderListByDriverView.as_view({'get': 'list'}),
        name='order_list_by_driver'),
    url(r'list/byTruck',
        OrderListByTruckView.as_view({'get': 'list'}),
        name='order_list_by_truck'),
    url(r'list',
        OrderListView.as_view({'get': 'list'}),
        name='order_list'),
]
