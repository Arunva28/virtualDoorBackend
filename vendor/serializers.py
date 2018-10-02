from rest_framework import serializers
from .models import VendorModel

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorModel
        fields = '__all__'