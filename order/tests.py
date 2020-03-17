from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase

from django.urls import reverse

from model_mommy import mommy

from driver.models import Driver
from order.models import Order
from location.models import Location
from truck.models import Truck


# Create your tests here.
class OrderTests(APITestCase):
    data = {
        'name': 'Lukas & Cia',
        'description': 'Joy delivery',
        'client_name': 'Lukas',
    }

    driver_data = {'full_name': 'Lukas Ferreira Machado',
                    'gender': 'M',
                    'cpf': '047.291.801-00',
                    'cnh': '83967543154',
                    'cnh_type': 'A',
                    'telephone': '61998649461',
                    'age': '25',
                    'birthday': '10/08/1994',
                    'has_vehicle': True,
                    'is_active': True}

    truck_data = {'truck_type': 1}

    origin_data = {'name': 'Lukas Home',
                    'location': {
                        "latitude": -15.800099560468379,
                        "longitude": -48.06286811159569
                    },
                    'address': 'Somewhere over the rainbow',
                    'zip_code': '72130130',
                    'city': 'Brasilia'}

    destiny_data = {'name': 'Fukus Home',
                    'location': {
                        "latitude": -15.838757276970728,
                        "longitude": -48.037472956647036
                    },
                    'address': 'Somewhere over the sky',
                    'zip_code': '71930250',
                    'city': 'Brasilia'}

    def test_order_create(self):
        data = self.data.copy()
        driver_data = self.driver_data.copy()
        truck_data = self.truck_data.copy()
        origin_data = self.origin_data.copy()
        destiny_data = self.destiny_data.copy()

        response = self.client.post(reverse(
            'driver:driver_create'), driver_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)

        response = self.client.post(reverse(
            'truck:truck_create'), truck_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Truck.objects.count(), 1)

        response = self.client.post(reverse(
            'location:location_create'), origin_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)

        response = self.client.post(reverse(
            'location:location_create'), destiny_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 2)

        data['driver'] = Driver.objects.last().id
        data['truck'] = Truck.objects.last().id
        data['origin'] = Location.objects.first().id
        data['destiny'] = Location.objects.last().id

        response = self.client.post(reverse(
            'order:order_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

    def test_order_properly_set(self):
        data = self.data.copy()
        driver_data = self.driver_data.copy()
        truck_data = self.truck_data.copy()
        origin_data = self.origin_data.copy()
        destiny_data = self.destiny_data.copy()

        response = self.client.post(reverse(
            'driver:driver_create'), driver_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)

        response = self.client.post(reverse(
            'truck:truck_create'), truck_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Truck.objects.count(), 1)

        response = self.client.post(reverse(
            'location:location_create'), origin_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)

        response = self.client.post(reverse(
            'location:location_create'), destiny_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 2)

        data['driver'] = Driver.objects.last()
        data['truck'] = Truck.objects.last()
        data['origin'] = Location.objects.first()
        data['destiny'] = Location.objects.first()

        with self.assertRaises(ValidationError):
            mommy.make(Order, **data)

    def test_order_update(self):
        data = self.data.copy()
        driver_data = self.driver_data.copy()
        truck_data = self.truck_data.copy()
        origin_data = self.origin_data.copy()
        destiny_data = self.destiny_data.copy()

        response = self.client.post(reverse(
            'driver:driver_create'), driver_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)

        response = self.client.post(reverse(
            'truck:truck_create'), truck_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Truck.objects.count(), 1)

        response = self.client.post(reverse(
            'location:location_create'), origin_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)

        response = self.client.post(reverse(
            'location:location_create'), destiny_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 2)

        data['driver'] = Driver.objects.last().id
        data['truck'] = Truck.objects.last().id
        data['origin'] = Location.objects.first().id
        data['destiny'] = Location.objects.last().id

        response = self.client.post(reverse(
            'order:order_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        data['name'] = 'Lala & Cia'

        response = self.client.put(reverse(
            'order:order_update_retrieve_delete',
            kwargs={'pk': Order.objects.last().id}
        ), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), data['name'])
        self.assertEqual(Order.objects.count(), 1)

    def test_order_retrieve(self):
        data = self.data.copy()
        driver_data = self.driver_data.copy()
        truck_data = self.truck_data.copy()
        origin_data = self.origin_data.copy()
        destiny_data = self.destiny_data.copy()

        response = self.client.post(reverse(
            'driver:driver_create'), driver_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)

        response = self.client.post(reverse(
            'truck:truck_create'), truck_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Truck.objects.count(), 1)

        response = self.client.post(reverse(
            'location:location_create'), origin_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)

        response = self.client.post(reverse(
            'location:location_create'), destiny_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 2)

        data['driver'] = Driver.objects.last().id
        data['truck'] = Truck.objects.last().id
        data['origin'] = Location.objects.first().id
        data['destiny'] = Location.objects.last().id

        response = self.client.post(reverse(
            'order:order_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        response = self.client.get(reverse(
            'order:order_update_retrieve_delete',
            kwargs={'pk': Order.objects.last().id}
        ), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), data['name'])
        self.assertEqual(Order.objects.count(), 1)

    def test_order_delete(self):
        data = self.data.copy()
        driver_data = self.driver_data.copy()
        truck_data = self.truck_data.copy()
        origin_data = self.origin_data.copy()
        destiny_data = self.destiny_data.copy()

        response = self.client.post(reverse(
            'driver:driver_create'), driver_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)

        response = self.client.post(reverse(
            'truck:truck_create'), truck_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Truck.objects.count(), 1)

        response = self.client.post(reverse(
            'location:location_create'), origin_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)

        response = self.client.post(reverse(
            'location:location_create'), destiny_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 2)

        data['driver'] = Driver.objects.last().id
        data['truck'] = Truck.objects.last().id
        data['origin'] = Location.objects.first().id
        data['destiny'] = Location.objects.last().id

        response = self.client.post(reverse(
            'order:order_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        response = self.client.delete(reverse(
            'order:order_update_retrieve_delete',
            kwargs={'pk': Order.objects.last().id}
        ), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)

    def test_order_list_by_driver(self):
        data = self.data.copy()
        driver_data = self.driver_data.copy()
        truck_data = self.truck_data.copy()
        origin_data = self.origin_data.copy()
        destiny_data = self.destiny_data.copy()

        response = self.client.post(reverse(
            'driver:driver_create'), driver_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)

        response = self.client.post(reverse(
            'truck:truck_create'), truck_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Truck.objects.count(), 1)

        response = self.client.post(reverse(
            'location:location_create'), origin_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)

        response = self.client.post(reverse(
            'location:location_create'), destiny_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 2)

        data['driver'] = Driver.objects.last().id
        data['truck'] = Truck.objects.last().id
        data['origin'] = Location.objects.first().id
        data['destiny'] = Location.objects.last().id

        response = self.client.post(reverse(
            'order:order_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        response = self.client.post(reverse(
            'order:order_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)

        response = self.client.get(reverse(
            'order:order_list_by_driver'
        ), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)
        self.assertEqual(Order.objects.count(), 2)

    def test_order_list_by_truck(self):
        data = self.data.copy()
        driver_data = self.driver_data.copy()
        truck_data = self.truck_data.copy()
        origin_data = self.origin_data.copy()
        destiny_data = self.destiny_data.copy()

        response = self.client.post(reverse(
            'driver:driver_create'), driver_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)

        response = self.client.post(reverse(
            'truck:truck_create'), truck_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Truck.objects.count(), 1)

        response = self.client.post(reverse(
            'location:location_create'), origin_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)

        response = self.client.post(reverse(
            'location:location_create'), destiny_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 2)

        data['driver'] = Driver.objects.last().id
        data['truck'] = Truck.objects.last().id
        data['origin'] = Location.objects.first().id
        data['destiny'] = Location.objects.last().id

        response = self.client.post(reverse(
            'order:order_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        response = self.client.post(reverse(
            'order:order_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)

        response = self.client.get(reverse(
            'order:order_list_by_truck'
        ), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)
        self.assertEqual(Order.objects.count(), 2)

    def test_order_list(self):
        data = self.data.copy()
        driver_data = self.driver_data.copy()
        truck_data = self.truck_data.copy()
        origin_data = self.origin_data.copy()
        destiny_data = self.destiny_data.copy()

        response = self.client.post(reverse(
            'driver:driver_create'), driver_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Driver.objects.count(), 1)

        response = self.client.post(reverse(
            'truck:truck_create'), truck_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Truck.objects.count(), 1)

        response = self.client.post(reverse(
            'location:location_create'), origin_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 1)

        response = self.client.post(reverse(
            'location:location_create'), destiny_data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Location.objects.count(), 2)

        data['driver'] = Driver.objects.last().id
        data['truck'] = Truck.objects.last().id
        data['origin'] = Location.objects.first().id
        data['destiny'] = Location.objects.last().id

        response = self.client.post(reverse(
            'order:order_create'), data,
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        response = self.client.get(reverse(
            'order:order_list'
        ), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)
        self.assertEqual(Order.objects.count(), 1)
