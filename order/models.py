import datetime as dt

from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from driver.models import Driver
from truck.models import Truck
from location.models import Location


class Order(models.Model):
    driver = models.ForeignKey(
        Driver,
        on_delete=models.PROTECT,
        verbose_name='Order Driver')
    truck = models.ForeignKey(
        Truck,
        on_delete=models.PROTECT,
        verbose_name='Order Truck')
    origin = models.ForeignKey(
        Location,
        related_name='orders_location_origin',
        on_delete=models.PROTECT,
        verbose_name='Origin Location')
    destiny = models.ForeignKey(
        Location,
        related_name='orders_location_destiny',
        on_delete=models.PROTECT,
        verbose_name='Destiny Location')
    name = models.CharField(
        max_length=100,
        verbose_name='Order Name')
    description = models.CharField(
        max_length=250,
        verbose_name='Order Description')
    client_name = models.CharField(
        max_length=100,
        verbose_name='Client Name')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Creation date')
    updated = models.DateTimeField(
        auto_now_add=True, verbose_name='Update date')

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        ordering = ['id']

        permissions = (
            ('detail_order', 'Can detail %s' % verbose_name),
            ('list_order', 'Can list %s' % verbose_name),
        )

    def validate_unique(self, exclude=None):
        if self.origin.location == self.destiny.location:
            raise ValidationError(
                _('Location must have different coordinates (%.14f, %.14f)') % self.origin.location.coords[::-1]
            )

    def save(self, *args, **kwargs):
        self.validate_unique()
        if not self.id:
            self.created = dt.date.today()
        self.updated = dt.datetime.today()

        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return '%s: (%s: %s (%s)) ' % (self.id, self.driver.cpf, self.name, self.destiny.zip_code)
