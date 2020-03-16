import datetime as dt

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from django.urls import reverse

from model_mommy import mommy

from driver.models import Driver

from utils import driver_properly_configured


# Create your tests here.
class DriverTests(APITestCase):
    data = {'full_name': 'Lukas Ferreira Machado',
            'gender': 'M',
            'cpf': '047.291.801-00',
            'cnh': '83967543154',
            'cnh_type': 'A',
            'telephone': '61998649461',
            'age': '25',
            'birthday': '10/08/1994',
            'has_vehicle': True,
            'is_active': True}

    def test_driver_properly_set(self):
        data = self.data.copy()

        data['cpf'] = '047.291.801-01'
        data['cnh'] = '83967543155'

        driver = mommy.make(Driver, **data)
        driver.save()

        with self.assertRaises(ValidationError):
            driver_properly_configured(driver)

    def test_create(self):
        data = self.data.copy()

        data['cpf'] = '047.291.801-01'
        response = self.client.post(reverse(
            'driver:driver_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['cpf'][0].__str__(), 'CPF must be valid.')
        self.assertEqual(Driver.objects.count(), 0)

        data['cpf'] = '047.291.801-00'
        data['cnh'] = '83967543155'
        response = self.client.post(reverse(
            'driver:driver_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['cnh'][0].__str__(), 'CNH must be valid.')
        self.assertEqual(Driver.objects.count(), 0)

        data['cnh'] = '83967543154'
        data['age'] = '17'
        response = self.client.post(reverse(
            'driver:driver_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['age'][0].__str__(),
                         'Certifque-se de que este valor seja maior ou igual a 18.')
        self.assertEqual(Driver.objects.count(), 0)

        data['age'] = '18'
        response = self.client.post(reverse(
            'driver:driver_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)

    def test_update(self):
        data = self.data.copy()

        response = self.client.post(reverse(
            'driver:driver_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)

        data['birthday'] = '10/08/1993'

        response = self.client.put(reverse(
            'driver:driver_update_retrieve_delete',
            kwargs={'pk': Driver.objects.last().id}
        ), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('birthday'), data['birthday'])
        self.assertEqual(Driver.objects.count(), 1)

    def test_list_has_vehicle(self):
        data = self.data.copy()

        response = self.client.post(reverse(
            'driver:driver_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)

        response = self.client.get(reverse(
            'driver:driver_has_vehicle_list'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)

        data['has_vehicle'] = False

        response = self.client.put(reverse(
            'driver:driver_update_retrieve_delete',
            kwargs={'pk': Driver.objects.last().id}
        ), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('has_vehicle'), False)
        self.assertEqual(Driver.objects.count(), 1)

        response = self.client.get(reverse(
            'driver:driver_has_vehicle_list'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 0)
