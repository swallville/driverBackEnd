import re
import datetime as dt

from django.db import transaction
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from validate_docbr import CPF, CNH

from driver.models import Driver, Register
from truck.models import Truck

from truck.serializers import TruckSerializer

from utils import CustomisedCharField, DATE_RANGE_INVALID, OPCS_GENDER, OPCS_CNH, ERROR_MESSAGES_CHOICE_FIELD, \
                  try_parsing_date


# Create your views here.
def get_driver_model_fields():
    array = [f.name for f in Driver._meta.fields + Driver._meta.many_to_many if f.name not in ['id']]
    return tuple(array)


def get_age(birthday):
    today = dt.date.today()
    born = birthday
    rest = 1 if (today.month, today.day) < (born.month, born.day) else 0
    return today.year - born.year - rest


class RegisterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = '__all__'


class DriverCreateSerializer(serializers.ModelSerializer):
    full_name = CustomisedCharField(
        max_length=100)

    gender = serializers.ChoiceField(
        choices=OPCS_GENDER,
        error_messages=ERROR_MESSAGES_CHOICE_FIELD
    )

    cpf = CustomisedCharField(
        max_length=14,
        validators=[UniqueValidator(queryset=Driver.objects.all())])

    cnh = CustomisedCharField(
        max_length=12,
        validators=[UniqueValidator(queryset=Driver.objects.all())])

    cnh_type = serializers.ChoiceField(
        choices=OPCS_CNH,
        error_messages=ERROR_MESSAGES_CHOICE_FIELD
    )

    telephone = CustomisedCharField(
        max_length=15)

    age = serializers.IntegerField(min_value=18)

    birthday = serializers.DateField(format='%d/%m/%Y', input_formats=['%d/%m/%Y', '%Y-%m-%d'])

    has_vehicle = serializers.BooleanField(default=False)

    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Driver
        exclude = ('id', 'registers')

        validators = [
            UniqueTogetherValidator(
                queryset=Driver.objects.all(),
                fields=('cpf', 'cnh'),
                message='Driver must have an unique CPF and CNH'
            )
        ]

    def validate_cpf(self, cpf):
        valid_cpf = CPF().validate(cpf)

        if not valid_cpf:
            raise serializers.ValidationError(_('CPF must be valid.'))

        if len(cpf) > 11:
            cpf = re.sub('[.-]', '', cpf)

        return cpf

    def validate_cnh(self, cnh):
        valid_cnh = CNH().validate(cnh)

        if not valid_cnh:
            raise serializers.ValidationError(_('CNH must be valid.'))

        return cnh

    def validate_birthday(self, birthday):
        if isinstance(birthday, str):
            return try_parsing_date(birthday)

        return birthday

    def validate_age(self, age):
        if age < 18:
            raise serializers.ValidationError(_('Age must be greater or equal 18.'))

        return age

    @transaction.atomic
    def save(self, **kwargs):
        cpf = self.validated_data.get('cpf', '')

        if len(cpf) > 11:
            cpf = re.sub('[.-]', '', cpf)

        birthday = self.validated_data.get('birthday', '')

        if isinstance(birthday, str):
            birthday = try_parsing_date(birthday)
            age = get_age(birthday)
        else:
            age = get_age(birthday)

        driver = Driver.objects.create(
            full_name=self.validated_data.get('full_name', ''),
            gender=self.validated_data.get('gender', ''),
            cpf=cpf,
            cnh=self.validated_data.get('cnh', ''),
            cnh_type=self.validated_data.get('cnh_type', ''),
            telephone=self.validated_data.get('telephone', ''),
            age=age,
            birthday=self.validated_data.get('birthday', ''),
            has_vehicle=self.validated_data.get('has_vehicle', ''),
            is_active=self.validated_data.get('is_active', ''),
        )

        driver.save()

        return driver


class DriverUpdateSerializer(serializers.ModelSerializer):
    full_name = CustomisedCharField(
        max_length=100)

    gender = serializers.ChoiceField(
        choices=OPCS_GENDER,
        error_messages=ERROR_MESSAGES_CHOICE_FIELD
    )

    cpf = CustomisedCharField(
        max_length=14,
        validators=[UniqueValidator(queryset=Driver.objects.all())])

    cnh = CustomisedCharField(
        max_length=12,
        validators=[UniqueValidator(queryset=Driver.objects.all())])

    cnh_type = serializers.ChoiceField(
        choices=OPCS_CNH,
        error_messages=ERROR_MESSAGES_CHOICE_FIELD
    )

    telephone = CustomisedCharField(
        max_length=15)

    age = serializers.IntegerField(min_value=18)

    birthday = serializers.DateField(format='%d/%m/%Y', input_formats=['%d/%m/%Y', '%Y-%m-%d'])

    has_vehicle = serializers.BooleanField(default=False)

    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = Driver
        exclude = ('id', 'registers')

        validators = [
            UniqueTogetherValidator(
                queryset=Driver.objects.all(),
                fields=('cpf', 'cnh'),
                message='Driver must have an unique CPF and CNH'
            )
        ]

    def validate_cpf(self, cpf):
        valid_cpf = CPF().validate(cpf)

        if not valid_cpf:
            raise serializers.ValidationError(_('CPF must be valid.'))

        if len(cpf) > 11:
            cpf = re.sub('[.-]', '', cpf)

        return cpf

    def validate_cnh(self, cnh):
        valid_cnh = CNH().validate(cnh)

        if not valid_cnh:
            raise serializers.ValidationError(_('CNH must be valid.'))

        return cnh

    def validate_birthday(self, birthday):
        if isinstance(birthday, str):
            return try_parsing_date(birthday)

        return birthday

    def validate_age(self, age):
        if age < 18:
            raise serializers.ValidationError(_('Age must be greater or equal 18.'))

        return age


class DriverListSerializer(serializers.ModelSerializer):
    registers = RegisterListSerializer(read_only=True, source='register_set', many=True)

    class Meta:
        model = Driver
        exclude = ('created', 'updated')


class RegisterSerializer(serializers.ModelSerializer):
    driver = serializers.PrimaryKeyRelatedField(queryset=Driver.objects.all())
    truck = serializers.PrimaryKeyRelatedField(queryset=Truck.objects.all())
    created = serializers.DateTimeField(read_only=True, format='%d/%m/%YT%H:%M:%S')
    updated = serializers.DateTimeField(read_only=True, format='%d/%m/%YT%H:%M:%S')
    is_Loaded = serializers.BooleanField(default=False)

    class Meta:
        model = Register
        fields = '__all__'


class RegisterListByTruckSerializer(serializers.ModelSerializer):
    truck = TruckSerializer(read_only=True)
    start_date = serializers.DateField(write_only=True, format='%d/%m/%Y', input_formats=['%d/%m/%Y', '%Y-%m-%d'])
    end_date = serializers.DateField(write_only=True, format='%d/%m/%Y', input_formats=['%d/%m/%Y', '%Y-%m-%d'])
    created = serializers.DateTimeField(read_only=True, format='%d/%m/%YT%H:%M:%S')
    updated = serializers.DateTimeField(read_only=True, format='%d/%m/%YT%H:%M:%S')

    def validate(self, data):
        """
        Check that the start date is before the end date.
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError({'error': DATE_RANGE_INVALID})
        return data

    class Meta:
        model = Register
        fields = ('truck', 'start_date', 'end_date', 'created', 'updated')
