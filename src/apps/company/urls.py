from django.urls import path

from .views import CompanyCreateView, CompanyListView,CompanyUpdateRetrieveDestroyView


urlpatterns = [
    path("", CompanyCreateView.as_view(), name="company-create-api-endpoint"),
    path("list/", CompanyListView.as_view(), name="company-list-api-endpoint"),
    path("<uuid:pk>", CompanyUpdateRetrieveDestroyView.as_view(), name="company-create-and-list-api-endpoint")
]