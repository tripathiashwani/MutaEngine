from rest_framework import generics, status, exceptions
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .serializers import CompanySerailizer
from .models import Company

class CompanyCreateListView(generics.ListCreateAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = CompanySerailizer

    def get_queryset(self):
        company = Company.objects.all()
        return company

    @extend_schema(
        request=OpenApiTypes.OBJECT,
        responses={201: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample(
                'Request',
                value={
                    "name": "string",
                    "address": "string",
                    "logo": "image file",
                    "email": "email",
                    "phone": "phone number",
                    "linkedin": "url"
                },
                request_only=True,
            ),
            OpenApiExample(
                'Response',
                value={
                    "status": "string",
                    "name": "string",
                    "address": "string",
                    "logo": "image file",
                    "email": "email",
                    "phone": "phone number",
                    "linkedin": "url"
                },
                response_only=True,
            ),
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        responses={200: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample(
                'Response',
                value={
                    "status": "string",
                    "name": "string",
                    "address": "string",
                    "logo": "image file",
                    "email": "email",
                    "phone": "phone number",
                    "linkedin": "url"
                },
                response_only=True,
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        company = Company.objects.all()
        serializer = self.get_serializer(instance=company,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CompanyUpdateRetrieveDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanySerailizer

    def get_queryset(self):
        company = Company.objects.all()
        return company

    def get_object(self):
        pk = self.kwargs.get('pk', None)
        if pk is None:
            raise exceptions.APIException("Comany id is required")
        
        try:
            company = Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise exceptions.APIException("Company not found")
        
        return company
    
    def get(self,request, *args, **kwargs):
        pk = self.kwargs.get('pk', None)
        if pk is None:
            raise exceptions.APIException("Comany id is required")
        
        try:
            company = Company.objects.get(pk=pk)
        except Company.DoesNotExist:
            raise exceptions.APIException("Company not found")

        serializer = self.get_serializer(instance=company)
        return Response(serializer.data, status=status.HTTP_200_OK)
        