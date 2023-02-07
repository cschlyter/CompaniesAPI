from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Company, Bank, BankAccount
from .serializers import CompanySerializer, BankSerializer, BankAccountSerializer


class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = (IsAuthenticated,)


class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = (IsAuthenticated,)


class BankList(generics.ListCreateAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = (IsAuthenticated,)


class BankDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = (IsAuthenticated,)


class BankAccountList(generics.ListCreateAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = (IsAuthenticated,)


class BankAccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = (IsAuthenticated,)
