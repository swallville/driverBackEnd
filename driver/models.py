from __future__ import unicode_literals
import datetime as dt

from django.contrib.gis.db import models
from django.db.models import Q
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from validate_docbr import CPF, CNH

from truck.models import Truck

from utils import OPCS_GENDER, OPCS_CNH, try_parsing_date


# Create your models here.
class Driver(models.Model):
    registers = models.ManyToManyField(
        Truck,
        through='Register',
        related_name='drivers',
        verbose_name='Registers'
    )
    full_name = models.CharField(
        max_length=100,
        verbose_name='Full Name')
    gender = models.CharField(
        max_length=2,
        verbose_name='Gender',
        choices=OPCS_GENDER)
    cpf = models.CharField(
        max_length=14,
        verbose_name='CPF',
        unique=True)
    cnh = models.CharField(
        max_length=12,
        verbose_name='CNH',
        unique=True)
    cnh_type = models.CharField(
        max_length=4,
        choices=OPCS_CNH,
        verbose_name='CNH Type')
    telephone = models.CharField(
        max_length=15,
        verbose_name='Telephone')
    age = models.PositiveSmallIntegerField(
        blank=True,
        verbose_name='Age',
        validators=[MinValueValidator(18)]
    )
    birthday = models.DateField(
        auto_now=False, auto_now_add=False, verbose_name='Birth date')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Creation date')
    updated = models.DateTimeField(
        auto_now_add=True, verbose_name='Update date')
    has_vehicle = models.BooleanField(
        default=False,
        verbose_name='Driver has vehicle?')
    is_active = models.BooleanField(
        default=True,
        verbose_name='Is active?')

    @property
    def drive_age(self):
        today = dt.date.today()

        if isinstance(self.birthday, str):
            self.birthday = try_parsing_date(self.birthday)
            born = self.birthday
        else:
            born = self.birthday

        rest = 1 if (today.month, today.day) < (born.month, born.day) else 0
        return today.year - born.year - rest

    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'
        ordering = ['full_name', 'cpf']

        permissions = (
            ('detail_driver', 'Can detail %s' % verbose_name),
            ('list_driver', 'Can list %s' % verbose_name),
        )

        constraints = [
            models.UniqueConstraint(fields=['cpf', 'cnh'], name='unique_driver'),
            models.CheckConstraint(check=Q(age__gte=18), name='age_gte_18')
        ]

    def clean(self):
        valid_cpf = CPF().validate(self.cpf)
        if not valid_cpf:
            raise ValidationError({
                'cpf': ValidationError(_('Invalid CPF %s.') % self.cpf, code='invalid'),
            })

        valid_cnh = CNH().validate(self.cnh)
        if not valid_cnh:
            raise ValidationError({
                'cnh': ValidationError(_('Invalid CNH %s.') % self.cnh, code='invalid'),
            })

    def validate_unique(self, exclude=None):
        qs = Driver.objects.filter(Q(cpf=self.cpf) | Q(cnh=self.cnh))
        if qs.count() > 1:
            raise ValidationError(
                _('Driver with CPF %s and CNH %s can be created just once!') % (self.cpf, self.cnh)
            )

    def save(self, *args, **kwargs):
        self.validate_unique()
        if not self.id:
            self.created = dt.date.today()
        self.updated = dt.datetime.today()

        self.age = self.drive_age

        super(Driver, self).save(*args, **kwargs)

    def __str__(self):
        return '%s - %s' % (self.cpf, self.full_name)


class Register(models.Model):
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        verbose_name='Register Driver')
    truck = models.ForeignKey(
        Truck,
        on_delete=models.CASCADE,
        verbose_name='Register Truck')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Creation date')
    updated = models.DateTimeField(
        auto_now_add=True, verbose_name='Update date')
    is_Loaded = models.BooleanField(
        default=False,
        verbose_name='Is loaded?')

    class Meta:
        verbose_name = 'Register'
        verbose_name_plural = 'Registers'
        ordering = ['-created']

        permissions = (
            ('detail_register', 'Can detail %s' % verbose_name),
            ('list_register', 'Can list %s' % verbose_name),
        )

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = dt.date.today()
        self.updated = dt.datetime.today()

        super(Register, self).save(*args, **kwargs)

    def __str__(self):
        return '%s - (%s): isLoaded=%s' % (self.id, self.driver.cpf, self.is_Loaded)
