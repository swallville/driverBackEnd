import datetime as dt

from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q
from django.db import transaction

from collections import OrderedDict

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from driver.models import Driver, Register
from driver.serializers import DriverCreateSerializer, DriverUpdateSerializer,\
    DriverListSerializer, RegisterSerializer, RegisterListByTruckSerializer

from utils import DATE_RANGE_INVALID, try_parsing_date, verify_date_range
# Create your views here.


class Pagination(PageNumberPagination):
    def paginate_queryset(self, queryset, request, view=None):
        self.count = queryset.count()

        return super(Pagination, self).paginate_queryset(queryset, request, view=view)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class DriverCreateView(mixins.CreateModelMixin,
                       viewsets.GenericViewSet):
    """
    A simple ViewSet for creating drivers.
    """
    queryset = Driver.objects.all().order_by('full_name')
    serializer_class = DriverCreateSerializer
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary='Driver creation request',
        responses={201: 'Driver created successfully.',
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request})

        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DriverUpdateRetrieveDeleteView(mixins.RetrieveModelMixin,
                                     mixins.UpdateModelMixin,
                                     mixins.DestroyModelMixin,
                                     viewsets.GenericViewSet):
    """
    A simple ViewSet for update, retrieve and delete drivers.
    """
    queryset = Driver.objects.all().order_by('full_name')
    serializer_class = DriverUpdateSerializer
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary='Driver retrieve request',
        responses={200: serializer_class,
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def retrieve(self, request, *args, **kwargs):
        return super(DriverUpdateRetrieveDeleteView, self).retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Driver update request',
        responses={200: serializer_class,
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super(DriverUpdateRetrieveDeleteView, self).update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Driver destroy request',
        responses={204: 'Driver deleted.',
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super(DriverUpdateRetrieveDeleteView, self).destroy(request, *args, **kwargs)


class DriverListView(mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    A simple ViewSet for listing drivers.
    """
    queryset = Driver.objects.all().order_by('full_name')
    serializer_class = DriverListSerializer
    pagination_class = Pagination
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        queryset = super(DriverListView, self).get_queryset().filter(is_active=True).order_by('cpf')

        return queryset

    @swagger_auto_schema(
        operation_summary='Driver list request',
        responses={200: serializer_class,
                   404: 'This URL does not exist.'},)
    def list(self, request, *args, **kwargs):
        return super(DriverListView, self).list(request, *args, **kwargs)


class DriverActiveAndLoadedListView(
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    A ViewSet for listing active and unloaded drivers.
    """
    queryset = Driver.objects.all().order_by('full_name')
    serializer_class = DriverListSerializer
    pagination_class = Pagination
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        queryset = super(DriverActiveAndLoadedListView, self).get_queryset().filter(
            Q(is_active=True) & Q(register__is_Loaded=False)).distinct().order_by('cpf')

        return queryset

    @swagger_auto_schema(
        operation_summary='Driver active and loaded list request',
        responses={200: serializer_class,
                   404: 'This URL does not exist.'},)
    def list(self, request, *args, **kwargs):
        return super(DriverActiveAndLoadedListView, self).list(request, *args, **kwargs)


class DriverHasVehicleNumberRetrieveView(
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    A ViewSet for listing active and unloaded drivers.
    """
    queryset = Driver.objects.all().order_by('full_name')
    serializer_class = DriverListSerializer
    pagination_class = Pagination
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        queryset = super(DriverHasVehicleNumberRetrieveView, self).get_queryset().filter(
            has_vehicle=True).distinct().order_by('cpf')

        return queryset

    @swagger_auto_schema(
        operation_summary='Driver has vehicle list request',
        responses={200: serializer_class,
                   404: 'This URL does not exist.'},)
    def list(self, request, *args, **kwargs):
        return super(DriverHasVehicleNumberRetrieveView, self).list(request, *args, **kwargs)


class RegisterCreateView(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    """
    A simple ViewSet for creating registers.
    """
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary='Register creation request',
        responses={201: 'Register created successfully.',
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        return super(RegisterCreateView, self).create(request, *args, **kwargs)


class RegisterUpdateRetrieveDeleteView(mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin,
                                       viewsets.GenericViewSet):
    """
    A simple ViewSet for update, retrieve and delete registers.
    """
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary='Register retrieve request',
        responses={200: serializer_class,
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def retrieve(self, request, *args, **kwargs):
        return super(RegisterUpdateRetrieveDeleteView, self).retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Register update request',
        responses={200: serializer_class,
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super(RegisterUpdateRetrieveDeleteView, self).update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Register destroy request',
        responses={204: 'Register deleted.',
                   400: 'Invalid request body.',
                   404: 'This URL does not exist.'})
    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        return super(RegisterUpdateRetrieveDeleteView, self).destroy(request, *args, **kwargs)


class RegisterListView(mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    """
    A simple ViewSet for listing registers.
    """
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
    pagination_class = Pagination
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        operation_summary='Register list request',
        responses={200: serializer_class,
                   404: 'This URL does not exist.'},)
    def list(self, request, *args, **kwargs):
        return super(RegisterListView, self).list(request, *args, **kwargs)


class RegisterListByTruckView(
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """
    A ViewSet for listing loaded registers' trucks.
    """
    queryset = Register.objects.all()
    serializer_class = RegisterListByTruckSerializer
    pagination_class = Pagination
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        start_date = self.request.data.get('start_date', dt.date.today())
        end_date = self.request.data.get('end_date', dt.date.today())

        if isinstance(start_date, str):
            start_date = try_parsing_date(start_date)

        if isinstance(end_date, str):
            end_date = try_parsing_date(end_date)

        verify_date_range(start_date, end_date)

        queryset = super(RegisterListByTruckView, self).get_queryset().filter(
            Q(is_Loaded=True) &
            Q(created__date__range=(start_date, end_date))).order_by(
            'truck__truck_type', 'created')

        return queryset

    @swagger_auto_schema(
        operation_summary='Trucks with loaded registers list request',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'start_date': openapi.Schema(type=openapi.TYPE_STRING,
                                             description='Start query date. Formats (d/m/Y, Y-m-d)'),
                'end_date': openapi.Schema(type=openapi.TYPE_STRING,
                                           description='End query date. Formats (d/m/Y, Y-m-d)'),
            }
        ),
        responses={200: serializer_class,
                   400: openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'error': openapi.Schema(type=openapi.TYPE_STRING, description=DATE_RANGE_INVALID),
                        }
                    ),
                   404: 'This URL does not exist.'},)
    def list(self, request, *args, **kwargs):
        return super(RegisterListByTruckView, self).list(request, *args, **kwargs)
