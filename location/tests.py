from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from location.models import Location


# Create your tests here.
class LocationTests(APITestCase):
    data = {'name': 'Lukas Home',
            'location': {
                "latitude": -15.800099560468379,
                "longitude": -48.06286811159569
            },
            'address': 'Somewhere over the rainbow',
            'zip_code': '72130130',
            'city': 'Brasilia'}

    def test_location_create(self):
        data = self.data.copy()

        response = self.client.post(reverse(
            'location:location_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)

    def test_location_update(self):
        data = self.data.copy()

        response = self.client.post(reverse(
            'location:location_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)

        data['name'] = 'Lukus Home'

        response = self.client.put(reverse(
            'location:location_update_retrieve_delete',
            kwargs={'pk': Location.objects.last().id}
        ), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), 'Lukus Home')
        self.assertEqual(Location.objects.count(), 1)

    def test_location_retrieve(self):
        data = self.data.copy()

        response = self.client.post(reverse(
            'location:location_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)

        response = self.client.get(reverse(
            'location:location_update_retrieve_delete',
            kwargs={'pk': Location.objects.last().id}
        ), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), 'Lukas Home')
        self.assertEqual(Location.objects.count(), 1)

    def test_location_delete(self):
        data = self.data.copy()

        response = self.client.post(reverse(
            'location:location_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)

        response = self.client.delete(reverse(
            'location:location_update_retrieve_delete',
            kwargs={'pk': Location.objects.last().id}
        ), format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Location.objects.count(), 0)

    def test_location_list(self):
        data = self.data.copy()

        response = self.client.post(reverse(
            'location:location_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)

        response = self.client.get(reverse(
            'location:location_list'
        ), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)
        self.assertEqual(Location.objects.count(), 1)
