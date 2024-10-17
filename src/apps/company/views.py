from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .models import Company
from .serializers import CompanySerializer

class CompanyDetailUpdateView(APIView):
    permission_classes = [IsAdminUser]  

    def get(self, request, *args, **kwargs):
       
        company = Company.objects.first()
        if not company:
            return Response({"error": "Company does not exist"}, status=status.HTTP_404_NOT_FOUND)

        
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        company = Company.objects.first()
        if not company:
            return Response({"error": "Company does not exist"}, status=status.HTTP_404_NOT_FOUND)

        
        serializer = CompanySerializer(company, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
