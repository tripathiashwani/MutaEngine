from django.urls import path

from .views import SMTPViewSet

urlpatterns = [
    path("", SMTPViewSet.as_view({"get": "list", "post": "create"}), name="smtp-list"),
    path("<uuid:pk>/", SMTPViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}), name="smtp-detail"),
]