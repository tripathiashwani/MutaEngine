from django.urls import path

from .views.job_views import OfferLetterTemplateViewSet

urlpatterns = [
    path("offer/letter/", OfferLetterTemplateViewSet.as_view({"get": "list", "post": "create"}), name="offer-letter-template-list"),
    path("offer/letter/<uuid:pk>/", OfferLetterTemplateViewSet.as_view({"get": "retrieve", "patch": "update", "put": "update", "delete": "destroy"}), name="offer-letter-template-detail"),
]