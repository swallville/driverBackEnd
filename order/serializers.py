from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from driver.models import Driver
from location.models import Location
from order.models import Order
from truck.models import Truck

from driver.serializers import DriverListSerializer
from location.serializers import LocationSerializer
from truck.serializers import TruckSerializer

from utils import CustomisedCharField


class OrderSerializer(serializers.ModelSerializer):
    name = CustomisedCharField(
        max_length=100)
    description = CustomisedCharField(
        max_length=250)
    client_name = CustomisedCharField(
        max_length=100)
    driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all())
    truck = serializers.PrimaryKeyRelatedField(queryset=Truck.objects.all())
    origin = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    destiny = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    created = serializers.DateTimeField(read_only=True, format='%d/%m/%YT%H:%M:%S')
    updated = serializers.DateTimeField(read_only=True, format='%d/%m/%YT%H:%M:%S')

    def validate(self, data):
        origin = data.get('origin')
        destiny = data.get('destiny')

        try:
            if origin.location == destiny.location:
                raise serializers.ValidationError(
                    _('Location must have different coordinates (%.14f, %.14f)') % origin.location.coords[::-1]
                )
        except AttributeError:
            return data

        return data

    class Meta:
        model = Order
        fields = '__all__'


class OrderListLocationsSerializer(serializers.ModelSerializer):
    origin = LocationSerializer()
    destiny = LocationSerializer()

    class Meta:
        model = Order
        fields = ('origin', 'destiny')


class OrderListSerializer(serializers.ModelSerializer):
    driver = DriverListSerializer()
    truck = TruckSerializer()
    origin = LocationSerializer()
    destiny = LocationSerializer()

    class Meta:
        model = Order
        exclude = ('created', 'updated')


class OrderListByDriverSerializer(serializers.ModelSerializer):
    driver = serializers.SerializerMethodField('get_driver_serialized')
    locations = serializers.SerializerMethodField('get_locations_serialized')

    def get_driver_serialized(self, obj):
        return DriverListSerializer(Driver.objects.get(id=obj['driver'])).data

    def get_locations_serialized(self, obj):
        array = [OrderListLocationsSerializer(item).data for item in Order.objects.filter(
            driver__id=obj['driver'], driver__is_active=True, created__exact=obj['max'])]

        return array

    class Meta:
        model = Order
        fields = ('driver', 'locations')


class OrderListByTruckSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(min_value=0)
    truck = serializers.SerializerMethodField('get_truck_serialized')
    locations = serializers.SerializerMethodField('get_locations_serialized')

    def get_truck_serialized(self, obj):
        return TruckSerializer(Truck.objects.get(id=obj['truck'])).data

    def get_locations_serialized(self, obj):
        array = [OrderListLocationsSerializer(item).data for item in Order.objects.filter(
            truck__truck_type=obj['truck'])]

        return array

    class Meta:
        model = Order
        fields = ('count', 'truck', 'locations')
