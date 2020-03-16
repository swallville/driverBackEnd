from rest_framework import mixins, viewsets

from django.db import transaction

from drf_yasg.utils import swagger_auto_schema

from truck.models import Truck

from truck.serializers import TruckSerializer


class TruckCreateView(mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    """
    A simple ViewSet for creating trucks.
    """
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary='Truck creation request',
        responses={201: 'Truck created successfully.',
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super(TruckCreateView, self).create(request, *args, **kwargs)


class TruckUpdateRetrieveDeleteView(mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.DestroyModelMixin,
                                    viewsets.GenericViewSet):
    """
    A simple ViewSet for update, retrieve and destroy trucks.
    """
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary='Truck retrieve request',
        responses={200: serializer_class,
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def retrieve(self, request, *args, **kwargs):
        return super(TruckUpdateRetrieveDeleteView, self).retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Truck update request',
        responses={200: serializer_class,
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super(TruckUpdateRetrieveDeleteView, self).update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Truck destroy request',
        responses={204: 'Truck deleted.',
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super(TruckUpdateRetrieveDeleteView, self).destroy(request, *args, **kwargs)


# Create your views here.
class TruckListView(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """
    A simple ViewSet for listing trucks.
    """
    queryset = Truck.objects.all().order_by('id')
    serializer_class = TruckSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        queryset = super(TruckListView, self).get_queryset()

        return queryset

    @swagger_auto_schema(
        operation_summary='Location list request',
        responses={200: serializer_class,
                   404: 'This URL does not exist.'},)
    def list(self, request, *args, **kwargs):
        return super(TruckListView, self).list(request, *args, **kwargs)
