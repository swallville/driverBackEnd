from rest_framework import mixins, viewsets

from django.db import transaction

from drf_yasg.utils import swagger_auto_schema

from location.models import Location

from location.serializers import LocationSerializer


# Create your views here.
class LocationCreateView(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """
    A simple ViewSet for creating locations.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary='Location creation request',
        responses={201: 'Location created successfully.',
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super(LocationCreateView, self).create(request, *args, **kwargs)


class LocationUpdateRetrieveDeleteView(mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin,
                                       viewsets.GenericViewSet):
    """
    A simple ViewSet for update, retrieve and delete locations.
    """
    queryset = Location.objects.all().order_by('full_name')
    serializer_class = LocationSerializer
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary='Location retrieve request',
        responses={200: serializer_class,
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def retrieve(self, request, *args, **kwargs):
        return super(LocationUpdateRetrieveDeleteView, self).retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Location update request',
        responses={200: serializer_class,
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super(LocationUpdateRetrieveDeleteView, self).update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Location destroy request',
        responses={204: 'Location deleted.',
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super(LocationUpdateRetrieveDeleteView, self).destroy(request, *args, **kwargs)


class LocationListView(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """
    A simple ViewSet for listing locations.
    """
    queryset = Location.objects.all().order_by('id')
    serializer_class = LocationSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        queryset = super(LocationListView, self).get_queryset()

        return queryset

    @swagger_auto_schema(
        operation_summary='Location list request',
        responses={200: serializer_class,
                   404: 'This URL does not exist.'},)
    def list(self, request, *args, **kwargs):
        return super(LocationListView, self).list(request, *args, **kwargs)
