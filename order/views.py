from rest_framework import mixins, viewsets

from django.db.models import Count, Max

from django.db import transaction

from drf_yasg.utils import swagger_auto_schema

from order.models import Order

from order.serializers import OrderSerializer, OrderListSerializer, OrderListByDriverSerializer,\
                             OrderListByTruckSerializer


class OrderCreateView(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    """
    A simple ViewSet for creating orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary='Order creation request',
        responses={201: 'Order created successfully.',
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super(OrderCreateView, self).create(request, *args, **kwargs)


class OrderUpdateRetrieveDeleteView(mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin,
                                    viewsets.GenericViewSet):
    """
    A simple ViewSet for update, retrieve and delete orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary='Order retrieve request',
        responses={200: serializer_class,
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def retrieve(self, request, *args, **kwargs):
        return super(OrderUpdateRetrieveDeleteView, self).retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Order update request',
        responses={200: serializer_class,
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super(OrderUpdateRetrieveDeleteView, self).update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Order destroy request',
        responses={204: 'Order deleted.',
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super(OrderUpdateRetrieveDeleteView, self).destroy(request, *args, **kwargs)


# Create your views here.
class OrderListView(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    A simple ViewSet for listing orders.
    """
    queryset = Order.objects.all().order_by('id')
    serializer_class = OrderListSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()

        return queryset

    @swagger_auto_schema(
        operation_summary='Order list request',
        responses={200: serializer_class,
                   404: 'This URL does not exist.'},)
    def list(self, request, *args, **kwargs):
        return super(OrderListView, self).list(request, *args, **kwargs)


class OrderListByDriverView(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """
    A ViewSet for listing drivers locations.
    """
    queryset = Order.objects.filter(driver__is_active=True).values('driver').annotate(
        count=Count('driver__id'), max=Max('created')).order_by('-count')
    serializer_class = OrderListByDriverSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        queryset = super(OrderListByDriverView, self).get_queryset()

        return queryset

    @swagger_auto_schema(
        operation_summary='Order list by driver request',
        responses={200: serializer_class,
                   404: 'This URL does not exist.'},)
    def list(self, request, *args, **kwargs):
        return super(OrderListByDriverView, self).list(request, *args, **kwargs)


class OrderListByTruckView(mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    """
    A ViewSet for listing orders by truck type.
    """
    queryset = Order.objects.values('truck').annotate(
        count=Count('truck__truck_type')).order_by('-count')
    serializer_class = OrderListByTruckSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        queryset = super(OrderListByTruckView, self).get_queryset()

        return queryset

    @swagger_auto_schema(
        operation_summary='Order list by truck request',
        responses={200: serializer_class,
                   404: 'This URL does not exist.'},)
    def list(self, request, *args, **kwargs):
        return super(OrderListByTruckView, self).list(request, *args, **kwargs)
