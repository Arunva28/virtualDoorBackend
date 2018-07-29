from rest_framework import serializers
from .models import SecurityOffice


class SeurityOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityOffice
        fields = '__all__'


class PrimaryKeyToSecuritySerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityOffice
        fields = ('user', 'Name', 'Unit', 'MobileNumber', 'VisitorMailID', 'Remarks', 'Time', 'Date', 'BuildingName')
