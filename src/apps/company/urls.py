from django.urls import path

from .views import CompanyCreateListView, CompanyUpdateRetrieveDestroyView


urlpatterns = [
    path("", CompanyCreateListView.as_view(), name="company-create-and-list-api-endpoint"),
    path("<uuid:pk>", CompanyUpdateRetrieveDestroyView.as_view(), name="company-create-and-list-api-endpoint")
]