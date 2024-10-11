from rest_framework.request import Request as DRFRequest

from src.apps.auth.models import User


class Request(DRFRequest):
    user: User
    data: dict