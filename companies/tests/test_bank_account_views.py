import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from companies.models import BankAccount
from companies.serializers import BankAccountSerializer
from companies.tests.factories import BankAccountFactory, BankFactory, CompanyFactory
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


client = Client()


class GetAllBankAccountsTest(TestCase):
    """ Test module for GET all Bank Account API """

    def setUp(self):
        BankAccountFactory.create_batch(5)
        self.user = User.objects.create_user('test_user', 'test@test.com', 'test123')
        self.token = Token.objects.create(user=self.user)

    def test_get_all_bank_accounts(self):
        # get API response
        response = client.get(
            reverse('bank_accounts_list'),
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        # get data from db
        bank_accounts = BankAccount.objects.all()
        serializer = BankAccountSerializer(bank_accounts, many=True)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleBankAccountTest(TestCase):
    """ Test module for GET single Bank Account API """

    def setUp(self):
        self.bank_account_1 = BankAccountFactory()
        self.user = User.objects.create_user('test_user', 'test@test.com', 'test123')
        self.token = Token.objects.create(user=self.user)

    def test_get_valid_single_bank_account(self):
        response = client.get(
            reverse('bank_accounts_detail', kwargs={'pk': self.bank_account_1.pk}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        bank_account = BankAccount.objects.get(pk=self.bank_account_1.pk)
        serializer = BankAccountSerializer(bank_account)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_bank_account(self):
        response = client.get(
            reverse('bank_accounts_detail', kwargs={'pk': 30}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewBankAccountTest(TestCase):
    """ Test module for inserting a new bank account """

    def setUp(self):
        self.company_1 = CompanyFactory()
        self.bank_1 = BankFactory()
        self.valid_payload = {
            'bank': self.bank_1.pk,
            'company': self.company_1.pk,
            'account_number': '102548758',
            'agency': '0024',
        }
        self.invalid_payload = {
            'name': '',
            'phone': '48995481447',
        }
        self.user = User.objects.create_user('test_user', 'test@test.com', 'test123')
        self.token = Token.objects.create(user=self.user)

    def test_create_valid_bank_account(self):
        response = client.post(
            reverse('bank_accounts_list'),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BankAccount.objects.count(), 1)
        self.assertEqual(BankAccount.objects.get().bank.id, self.bank_1.id)
        self.assertEqual(BankAccount.objects.get().company.id, self.company_1.id)
        self.assertEqual(BankAccount.objects.get().account_number, json.loads(response.content)["account_number"])
        self.assertEqual(BankAccount.objects.get().agency, json.loads(response.content)["agency"])

    def test_create_invalid_bank_account(self):
        response = client.post(
            reverse('bank_accounts_list'),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateSingleBankAccountTest(TestCase):
    """ Test module for updating an existing bank account record """

    def setUp(self):
        self.bank_account_1 = BankAccountFactory()

        self.valid_payload = {
            'bank': self.bank_account_1.bank.pk,
            'company': self.bank_account_1.company.pk,
            'account_number': '102548758',
            'agency': '0024',
        }
        self.invalid_payload = {
            'name': '',
            'phone': '48995481447',
        }
        self.user = User.objects.create_user('test_user', 'test@test.com', 'test123')
        self.token = Token.objects.create(user=self.user)

    def test_valid_update_bank_account(self):
        response = client.put(
            reverse('bank_accounts_detail', kwargs={'pk': self.bank_account_1.pk}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BankAccount.objects.get().bank.id, self.bank_account_1.bank.id)
        self.assertEqual(BankAccount.objects.get().company.id, self.bank_account_1.company.id)
        self.assertEqual(BankAccount.objects.get().account_number, json.loads(response.content)["account_number"])
        self.assertEqual(BankAccount.objects.get().agency, json.loads(response.content)["agency"])

    def test_invalid_update_bank_account(self):
        response = client.put(
            reverse('bank_accounts_detail', kwargs={'pk': self.bank_account_1.pk}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleBankAccountTest(TestCase):
    """ Test module for deleting an existing bank account record """

    def setUp(self):
        self.bank_account_1 = BankAccountFactory()
        self.user = User.objects.create_user('test_user', 'test@test.com', 'test123')
        self.token = Token.objects.create(user=self.user)

    def test_valid_delete_bank_account(self):
        response = client.delete(
            reverse('bank_accounts_detail', kwargs={'pk': self.bank_account_1.pk}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_bank_account(self):
        response = client.delete(
            reverse('bank_accounts_detail', kwargs={'pk': 30}),
            HTTP_AUTHORIZATION=f'Token {self.token.key}',
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
