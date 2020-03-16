from rest_framework import serializers

from truck.models import Truck

from utils import OPCS_TRUCK


class TruckSerializer(serializers.ModelSerializer):
    truck_type = serializers.ChoiceField(
        choices=OPCS_TRUCK,
        label='Truck types')

    class Meta:
        model = Truck
        fields = '__all__'
