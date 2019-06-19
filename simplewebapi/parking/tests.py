from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_api_key.models import APIKey
from parking.models import CarParks

api_client = APIClient()

class CarParkModelTest(TestCase):

    def test_whatever_creation(self):
        """Test to see that we can successfully create a CarPark object
        with the model - needs further tests for invalid data"""
        CarParks.objects.all().delete()

        carparkobj = CarParks.objects.create(
            carpark_id = 1,
            name = "a carpark 1",
            address = "an address",
            postcode = "XY1 1XY",
            location = "nowhere",
            spaces = 100,
            min_cost_pence = 100,
            features = {"park_and_ride":True,"electric_car_charge_point":False},
            operator = "an operator"
        )
        self.assertTrue(isinstance(carparkobj, CarParks))
        self.assertEqual(carparkobj.name, "a carpark 1")

class CarParksTestCase(TestCase):
    def setUp(self):
        CarParks.objects.all().delete()

        self.api_key, self.generated_key = APIKey.objects.create_key(name="parking")

        for count in range(37):
            park_and_ride = True if count == 1 or count == 2 else False
            charge_point = True if count == 2 or count == 3 else False

            CarParks.objects.create(
                carpark_id = count,
                name = "a carpark "+str(count),
                address = "an address",
                postcode = "XY1 1XY",
                location = "nowhere",
                spaces = 100,
                min_cost_pence = 100,
                features = {"park_and_ride":park_and_ride,"electric_car_charge_point":charge_point},
                operator = "an operator"
            )

    def test_404_if_wrong_url(self):
        """Test to see if we get a 404 back with random URL"""
        api_client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.generated_key)
        response = api_client.get('/asdfasdf/')   
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fails_without_auth(self):
        """Test to see if fails with missing Authorization header"""
        response = api_client.get('/carparks/')   
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_fails_with_invalid_auth(self):
        """Test to see if fails with invalid API key"""
        api_client.credentials(HTTP_AUTHORIZATION='Api-Key ' + "lkajsdfoijwe.oj3298rihfwieohf")
        response = api_client.get('/carparks/')   
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_all_entries_returned(self):
        """Test to see if we get a 200 response back with an array of 20 items as we expect?"""
        api_client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.generated_key)
        response = api_client.get('/carparks/')   
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 20)
        self.assertEqual(response.data['results'][0]['name'], "a carpark 0")

    def test_paging_is_twenty(self):
        """Test to see if we get a 200 response and remaining items in paging"""
        api_client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.generated_key)
        response = api_client.get('/carparks/?limit=20&offset=20')   
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 17)

    def test_query_filters(self):
        """Test our 'features' filters, and combinations of them"""
        api_client.credentials(HTTP_AUTHORIZATION='Api-Key ' + self.generated_key)
        response = api_client.get('/carparks/?park_and_ride=True')   
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        response = api_client.get('/carparks/?electric_car_charge_point=True')   
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        response = api_client.get('/carparks/?electric_car_charge_point=True&park_and_ride=True')   
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)