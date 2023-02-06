import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from companies.models import Company
from companies.serializers import CompanySerializer
from companies.tests.factories import CompanyFactory


client = Client()


class GetAllCompaniesTest(TestCase):
    """ Test module for GET all Companies API """

    def setUp(self):
        CompanyFactory.create_batch(5)

    def test_get_all_companies(self):
        # get API response
        response = client.get(reverse('company_list'))
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

    def test_get_valid_single_company(self):
        response = client.get(
            reverse('company_detail', kwargs={'pk': self.company_1.pk}))
        company = Company.objects.get(pk=self.company_1.pk)
        serializer = CompanySerializer(company)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_company(self):
        response = client.get(
            reverse('company_detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewCompanyTest(TestCase):
    """ Test module for inserting a new Company """

    def setUp(self):
        self.valid_payload = {
            'name': 'Copper Wire',
            'phone': '48995481447',
            'address': 'address test',
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

    def test_create_valid_company(self):
        response = client.post(
            reverse('company_list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_company(self):
        response = client.post(
            reverse('company_list'),
            data=json.dumps(self.invalid_phone_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_company_validates_phone_number(self):
        response = client.post(
            reverse('company_list'),
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
            'earnings_declared': 1,
        }
        self.invalid_payload = {
            'name': '',
            'phone': 'SADF2',
        }

    def test_valid_update_company(self):
        response = client.put(
            reverse('company_detail', kwargs={'pk': self.company_1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_company(self):
        response = client.put(
            reverse('company_detail', kwargs={'pk': self.company_1.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleCompanyTest(TestCase):
    """ Test module for deleting an existing Company record """

    def setUp(self):
        self.company_1 = CompanyFactory()

    def test_valid_delete_company(self):
        response = client.delete(
            reverse('company_detail', kwargs={'pk': self.company_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_company(self):
        response = client.delete(
            reverse('company_detail', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
