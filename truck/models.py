from __future__ import unicode_literals

from django.contrib.gis.db import models

from utils import OPCS_TRUCK


# Create your models here.
class Truck(models.Model):
    truck_type = models.CharField(
        max_length=2,
        verbose_name='Truck Type',
        choices=OPCS_TRUCK)

    class Meta:
        verbose_name = 'Truck'
        verbose_name_plural = 'Trucks'
        ordering = ['id']

        permissions = (
            ('detail_truck', 'Can detail %s' % verbose_name),
            ('list_truck', 'Can list %s' % verbose_name),
        )

    def __str__(self):
        return '%s - %s' % (self.id, self.get_truck_type_display())
