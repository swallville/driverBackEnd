from rest_framework import serializers

from drf_extra_fields.geo_fields import PointField

from location.models import Location

from utils import CustomisedCharField


def get_location_model_fields():
    black_list = ['id', 'location']
    array = [f.name for f in Location._meta.fields + Location._meta.many_to_many if f.name not in black_list]
    array.append('latitude')
    array.append('longitude')

    return tuple(array)


class LocationSerializer(serializers.ModelSerializer):
    name = CustomisedCharField(
        max_length=100)
    location = PointField()
    address = CustomisedCharField(
        max_length=100)
    zip_code = CustomisedCharField(
        max_length=9)
    city = CustomisedCharField(
        max_length=100)

    class Meta:
        model = Location
        fields = '__all__'
