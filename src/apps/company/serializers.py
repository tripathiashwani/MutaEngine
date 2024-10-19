
from rest_framework import serializers
from .models import Company,Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

class CompanySerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Company
        fields = "__all__"

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        if address_data:
            address_serializer = AddressSerializer(instance.address, data=address_data, partial=True)
            if address_serializer.is_valid():
                address_serializer.save()

        return super().update(instance, validated_data)
