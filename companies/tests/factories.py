import factory
from companies.models import Bank, Company, BankAccount

class BankFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bank

    code = factory.Faker("pystr", min_chars=3, max_chars=3)
    name = factory.Faker("company")

class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker("company")
    phone = factory.Faker("phone_number")
    address = factory.Faker("address")
    address_additional_info = factory.Faker("address")
    city = factory.Faker("city")
    state = factory.Faker("state")
    country = factory.Faker("country")
    earnings_declared = factory.Faker("pydecimal", left_digits=15, right_digits=4, positive=True)

class BankAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BankAccount

    bank = factory.SubFactory(BankFactory)
    company = factory.SubFactory(CompanyFactory)
    account_number = factory.Faker("pystr", min_chars=10, max_chars=10)
    agency = factory.Faker("pystr", min_chars=8, max_chars=8)
