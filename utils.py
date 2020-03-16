import datetime as dt

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.utils.translation import ugettext_lazy as _

from validate_docbr import CPF, CNH

DATE_FORMAT_INVALID = 'This date is not in a valid format.'

DATE_RANGE_INVALID = 'This date range is not a valid range.'

OPCS_GENDER = [('M', 'Male'), ('F', 'Female'), ('O', 'Others')]

OPCS_CNH = [('ACC', 'Category ACC'), ('A', 'Category A'), ('B', 'Category B'), ('C', 'Category C'),
            ('D', 'Category D'), ('E', 'Category E')]

OPCS_TRUCK = [('1', 'Caminhão 3/4'), ('2', 'Caminhão Toco'), ('3', 'Caminhão Truck'), ('4', 'Carreta Simples'),
            ('5', 'Carreta Eixo Extendido')]

ERROR_MESSAGES_CHOICE_FIELD = {
    'blank': 'This field is required.',
    'null': 'This field is required.',
    'invalid_choice': 'Invalid Information.'
}


def try_parsing_date(text):
    for fmt in ('%Y-%m-%d', '%d/%m/%Y'):
        try:
            return dt.datetime.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError({'error': DATE_FORMAT_INVALID})


def verify_date_range(start_date, end_date):
    invalid_range = True if end_date < start_date else False

    if invalid_range:
        raise ValidationError({'error': DATE_RANGE_INVALID})

    return invalid_range


def driver_properly_configured(driver):
    valid_cpf = CPF().validate(driver.cpf)

    if not valid_cpf:
        raise serializers.ValidationError(_('CPF must be valid.'))

    valid_cnh = CNH().validate(driver.cnh)

    if not valid_cnh:
        raise serializers.ValidationError(_('CNH must be valid.'))


class CustomisedCharField(serializers.CharField):
    default_error_messages = {
        'invalid': _('This information is not valid.'),
        'blank': _('This filed cannot be empty.'),
        'null': _('This filed cannot be null.'),
        'max_length': _('This filed can have at most {max_length} characters.'),
        'min_length': _('This filed must have at least {min_length} characters.')
    }
