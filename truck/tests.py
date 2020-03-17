from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from truck.models import Truck


# Create your tests here.
class TruckTests(APITestCase):
    data = {'truck_type': '1'}

    def test_truck_create(self):
        data = self.data.copy()

        response = self.client.post(reverse(
            'truck:truck_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Truck.objects.count(), 1)

    def test_truck_update(self):
        data = self.data.copy()

        response = self.client.post(reverse(
            'truck:truck_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Truck.objects.count(), 1)

        data['truck_type'] = '2'

        response = self.client.put(reverse(
            'truck:truck_update_retrieve_delete',
            kwargs={'pk': Truck.objects.last().id}
        ), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('truck_type'), '2')
        self.assertEqual(Truck.objects.count(), 1)

    def test_truck_retrieve(self):
        data = self.data.copy()

        response = self.client.post(reverse(
            'truck:truck_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Truck.objects.count(), 1)

        response = self.client.get(reverse(
            'truck:truck_update_retrieve_delete',
            kwargs={'pk': Truck.objects.last().id}
        ), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('truck_type'), '1')
        self.assertEqual(Truck.objects.count(), 1)

    def test_truck_delete(self):
        data = self.data.copy()

        response = self.client.post(reverse(
            'truck:truck_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Truck.objects.count(), 1)

        response = self.client.delete(reverse(
            'truck:truck_update_retrieve_delete',
            kwargs={'pk': Truck.objects.last().id}
        ), format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Truck.objects.count(), 0)

    def test_truck_list(self):
        data = self.data.copy()

        response = self.client.post(reverse(
            'truck:truck_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Truck.objects.count(), 1)

        response = self.client.get(reverse(
            'truck:truck_list'
        ), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)
        self.assertEqual(Truck.objects.count(), 1)

        data = self.data.copy()

        response = self.client.post(reverse(
            'truck:truck_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Truck.objects.count(), 2)

        response = self.client.get(reverse(
            'truck:truck_list'
        ), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 2)
        self.assertEqual(Truck.objects.count(), 2)
