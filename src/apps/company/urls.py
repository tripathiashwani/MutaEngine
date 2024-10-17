from django.urls import path
from .views import CompanyDetailUpdateView

urlpatterns = [
    path('api/company/', CompanyDetailUpdateView.as_view(), name='company-detail-update'),
]
