from django.urls import path
from .views import CompanyList, CompanyDetail, BankList, BankDetail, BankAccountList, BankAccountDetail

urlpatterns = [
    path("companies/", CompanyList.as_view(), name="company_list"),
    path("companies/<int:pk>/", CompanyDetail.as_view(), name="company_detail"),
    path("banks/", BankList.as_view(), name="bank_list"),
    path("banks/<int:pk>/", BankDetail.as_view(), name="bank_detail"),
    path("bank_accounts/", BankAccountList.as_view(), name="bank_accounts_list"),
    path("bank_accounts/<int:pk>/", BankAccountDetail.as_view(), name="bank_accounts_detail"),
]
