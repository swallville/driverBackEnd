from django.contrib.gis.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Location (models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Name of Location')
    location = models.PointField(
        verbose_name='Coordinates of Location'
    )
    address = models.CharField(
        max_length=100,
        verbose_name='Address of Location')
    zip_code = models.CharField(
        max_length=9,
        verbose_name='Zip code of Location')
    city = models.CharField(
        max_length=100,
        verbose_name='City of Location')

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        ordering = ['address']

        permissions = (
            ('detail_location', 'Can detail %s' % verbose_name),
            ('list_location', 'Can list %s' % verbose_name),
        )

        constraints = [
            models.UniqueConstraint(fields=['location'], name='unique_location'),
        ]

    def validate_unique(self, exclude=None):
        qs = Location.objects.filter(Q(location=self.location))
        if qs.count() > 1:
            raise ValidationError(
                _('Location must have different coordinates (%.14f, %.14f)') % self.location.coords[::-1]
            )

    def save(self, *args, **kwargs):
        self.validate_unique()

        super(Location, self).save(*args, **kwargs)

    def __str__(self):
        return '%s - %s' % (self.city, self.address)
