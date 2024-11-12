from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .models import Company
from .serializers import CompanySerializer
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

class CompanyDetailUpdateView(APIView):
    permission_classes = []
    authentication_classes = []

    @extend_schema(
        request=OpenApiTypes.OBJECT,
        responses={200: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample(
                'Request',
                value={
                    "name": "string",
                    "description": "string",
                    "address": {
                        "street": "string",
                        "city": "string",
                        "state": "string",
                        "postal_code": "string",
                        "country": "string"
                    },
                    "logo": "image file",
                    "email": "email",
                    "phone": "string",
                    "linkedin": "url",
                    "location": "url",
                    "founded_date": "YYYY-MM-DD",
                    "industry": "string",
                    "number_of_employees": 100,
                    "website": "url",
                    "facebook": "url",
                    "twitter": "url",
                    "instagram": "url"
                },
                request_only=True,
            ),
            OpenApiExample(
                'Response',
                value={
                    "status": "success",
                    "name": "string",
                    "description": "string",
                    "address": {
                        "street": "string",
                        "city": "string",
                        "state": "string",
                        "postal_code": "string",
                        "country": "string"
                    },
                    "logo": "image file",
                    "email": "email",
                    "phone": "string",
                    "linkedin": "url",
                    "location": "url",
                    "founded_date": "YYYY-MM-DD",
                    "industry": "string",
                    "number_of_employees": 100,
                    "website": "url",
                    "facebook": "url",
                    "twitter": "url",
                    "instagram": "url"
                },
                response_only=True,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        company = Company.objects.first()
        if not company:
            return Response({"error": "Company does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        request=OpenApiTypes.OBJECT,
        responses={200: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample(
                'Request',
                value={
                    "name": "string",
                    "description": "string",
                    "address": {
                        "street": "string",
                        "city": "string",
                        "state": "string",
                        "postal_code": "string",
                        "country": "string"
                    },
                    "logo": "image file",
                    "email": "email",
                    "phone": "string",
                    "linkedin": "url",
                    "location": "url",
                    "founded_date": "YYYY-MM-DD",
                    "industry": "string",
                    "number_of_employees": 100,
                    "website": "url",
                    "facebook": "url",
                    "twitter": "url",
                    "instagram": "url"
                },
                request_only=True,
            ),
            OpenApiExample(
                'Response',
                value={
                    "status": "success",
                    "name": "string",
                    "description": "string",
                    "address": {
                        "street": "string",
                        "city": "string",
                        "state": "string",
                        "postal_code": "string",
                        "country": "string"
                    },
                    "logo": "image file",
                    "email": "email",
                    "phone": "string",
                    "linkedin": "url",
                    "location": "url",
                    "founded_date": "YYYY-MM-DD",
                    "industry": "string",
                    "number_of_employees": 100,
                    "website": "url",
                    "facebook": "url",
                    "twitter": "url",
                    "instagram": "url"
                },
                response_only=True,
            ),
        ]
    )
    def patch(self, request, *args, **kwargs):
        company = Company.objects.first()
        if not company:
            return Response({"error": "Company does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
