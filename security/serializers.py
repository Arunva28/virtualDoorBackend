from rest_framework import serializers
from .models import SecurityOffice
from userinfo.models import BasicUserInfo
from userinfo.serializers import BasicUserSerializer

class SeurityOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityOffice
        fields = '__all__'

class PrimaryKeyToSecuritySerializer(serializers.ModelSerializer):
    #user = PrimaryKeySerializer(required=True)
    class Meta:
        model = SecurityOffice
        fields = ('user', 'Name', 'Unit', 'MobileNumber', 'VisitorMailID', 'Remarks', 'Time', 'Date')
