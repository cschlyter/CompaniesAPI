from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Bank(models.Model):
    code = models.CharField(max_length=3)
    name = models.TextField(max_length=255)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.TextField(max_length=255)
    phone = PhoneNumberField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    earnings_declared = models.DecimalField(max_digits=19, decimal_places=4)
    bank_accounts = models.ManyToManyField(Bank, through='BankAccount')

    def __str__(self):
        return self.name


class BankAccount(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10)
    agency = models.CharField(max_length=8)

    def __str__(self):
        return self.account_number
