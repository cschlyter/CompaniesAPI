import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from companies.models import Company
from companies.serializers import CompanySerializer
from companies.tests.factories import CompanyFactory
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


client = Client()


class GetAllCompaniesTest(TestCase):
    """ Test module for GET all Companies API """

    def setUp(self):
        CompanyFactory.create_batch(5)
        self.user = User.objects.create_user('test_user', 'test@test.com', 'test123')
        self.token = Token.objects.create(user=self.user)

    def test_get_all_companies(self):
        # get API response
        response = client.get(
            reverse('company_list'),
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        # get data from db
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleCompaniesTest(TestCase):
    """ Test module for GET single Companies API """

    def setUp(self):
        self.company_1 = CompanyFactory()
        self.user = User.objects.create_user('test_user', 'test@test.com', 'test123')
        self.token = Token.objects.create(user=self.user)

    def test_get_valid_single_company(self):
        response = client.get(
            reverse('company_detail', kwargs={'pk': self.company_1.pk}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        company = Company.objects.get(pk=self.company_1.pk)
        serializer = CompanySerializer(company)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_company(self):
        response = client.get(
            reverse('company_detail', kwargs={'pk': 30}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewCompanyTest(TestCase):
    """ Test module for inserting a new Company """

    def setUp(self):
        self.valid_payload = {
            'name': 'Copper Wire',
            'phone': '48995481447',
            'address': 'address test',
            'city': 'address test',
            'state': 'address test',
            'country': 'address test',
            'earnings_declared': 1,
        }
        self.invalid_payload = {
            'name': '',
            'phone': '48995481447',
        }
        self.invalid_phone_payload = {
            'name': 'Copper Wire',
            'phone': 'test',
            'address': 'address test',
            'earnings_declared': 1,
        }
        self.user = User.objects.create_user('test_user', 'test@test.com', 'test123')
        self.token = Token.objects.create(user=self.user)

    def test_create_valid_company(self):
        response = client.post(
            reverse('company_list'),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(Company.objects.get().name, json.loads(response.content)["name"])
        self.assertEqual(Company.objects.get().phone, json.loads(response.content)["phone"])
        self.assertEqual(Company.objects.get().address, json.loads(response.content)["address"])
        self.assertEqual(Company.objects.get().address_additional_info, json.loads(response.content)["address_additional_info"])
        self.assertEqual(Company.objects.get().city, json.loads(response.content)["city"])
        self.assertEqual(Company.objects.get().state, json.loads(response.content)["state"])
        self.assertEqual(Company.objects.get().country, json.loads(response.content)["country"])
        self.assertEqual(str(Company.objects.get().earnings_declared), json.loads(response.content)["earnings_declared"])
        self.assertIsNotNone(Company.objects.get().created_at)

    def test_create_invalid_company(self):
        response = client.post(
            reverse('company_list'),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
            data=json.dumps(self.invalid_phone_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_company_validates_phone_number(self):
        response = client.post(
            reverse('company_list'),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleCompanyTest(TestCase):
    """ Test module for updating an existing Company record """

    def setUp(self):
        self.company_1 = CompanyFactory()

        self.valid_payload = {
            'name': 'Copper Wire',
            'phone': '48995481447',
            'address': 'address test',
            'city': 'address test',
            'state': 'address test',
            'country': 'address test',
            'earnings_declared': 1,
        }
        self.invalid_payload = {
            'name': '',
            'phone': 'SADF2',
        }
        self.user = User.objects.create_user('test_user', 'test@test.com', 'test123')
        self.token = Token.objects.create(user=self.user)

    def test_valid_update_company(self):
        response = client.put(
            reverse('company_detail', kwargs={'pk': self.company_1.pk}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_company(self):
        response = client.put(
            reverse('company_detail', kwargs={'pk': self.company_1.pk}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleCompanyTest(TestCase):
    """ Test module for deleting an existing Company record """

    def setUp(self):
        self.company_1 = CompanyFactory()
        self.user = User.objects.create_user('test_user', 'test@test.com', 'test123')
        self.token = Token.objects.create(user=self.user)

    def test_valid_delete_company(self):
        response = client.delete(
            reverse('company_detail', kwargs={'pk': self.company_1.pk}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_company(self):
        response = client.delete(
            reverse('company_detail', kwargs={'pk': 30}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
