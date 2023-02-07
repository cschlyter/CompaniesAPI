import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from companies.models import Bank
from companies.serializers import BankSerializer
from companies.tests.factories import BankFactory
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


client = Client()


class GetAllBanksTest(TestCase):
    """ Test module for GET all Banks API """

    def setUp(self):
        BankFactory.create_batch(5)
        self.user = User.objects.create_user('test_user', 'test@test.com', 'test123')
        self.token = Token.objects.create(user=self.user)

    def test_get_all_banks(self):
        # get API response
        response = client.get(
            reverse('bank_list'),
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        # get data from db
        banks = Bank.objects.all()
        serializer = BankSerializer(banks, many=True)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleBanksTest(TestCase):
    """ Test module for GET single Banks API """

    def setUp(self):
        self.bank_1 = BankFactory()
        self.user = User.objects.create_user('test_user', 'test@test.com', 'test123')
        self.token = Token.objects.create(user=self.user)

    def test_get_valid_single_bank(self):
        response = client.get(
            reverse('bank_detail', kwargs={'pk': self.bank_1.pk}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        bank = Bank.objects.get(pk=self.bank_1.pk)
        serializer = BankSerializer(bank)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_bank(self):
        response = client.get(
            reverse('bank_detail', kwargs={'pk': 30}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewBankTest(TestCase):
    """ Test module for inserting a new bank """

    def setUp(self):
        self.valid_payload = {
            'name': 'Copper Wire',
            'code': '002',
        }
        self.invalid_payload = {
            'name': '',
            'phone': '48995481447',
        }
        self.user = User.objects.create_user('test_user', 'test@test.com', 'test123')
        self.token = Token.objects.create(user=self.user)

    def test_create_valid_bank(self):
        response = client.post(
            reverse('bank_list'),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bank.objects.count(), 1)
        self.assertEqual(Bank.objects.get().name, json.loads(response.content)["name"])
        self.assertEqual(Bank.objects.get().code, json.loads(response.content)["code"])

    def test_create_invalid_bank(self):
        response = client.post(
            reverse('bank_list'),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSinglebankTest(TestCase):
    """ Test module for updating an existing bank record """

    def setUp(self):
        self.bank_1 = BankFactory()

        self.valid_payload = {
            'name': 'Copper Wire',
            'code': '002',
        }
        self.invalid_payload = {
            'name': '',
            'phone': '48995481447',
        }
        self.user = User.objects.create_user('test_user', 'test@test.com', 'test123')
        self.token = Token.objects.create(user=self.user)

    def test_valid_update_bank(self):
        response = client.put(
            reverse('bank_detail', kwargs={'pk': self.bank_1.pk}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_bank(self):
        response = client.put(
            reverse('bank_detail', kwargs={'pk': self.bank_1.pk}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSinglebankTest(TestCase):
    """ Test module for deleting an existing bank record """

    def setUp(self):
        self.bank_1 = BankFactory()
        self.user = User.objects.create_user('test_user', 'test@test.com', 'test123')
        self.token = Token.objects.create(user=self.user)

    def test_valid_delete_bank(self):
        response = client.delete(
            reverse('bank_detail', kwargs={'pk': self.bank_1.pk}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_bank(self):
        response = client.delete(
            reverse('bank_detail', kwargs={'pk': 30}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
