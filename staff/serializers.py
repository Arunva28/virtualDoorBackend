from rest_framework import serializers
from .models import StaffModel

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffModel
        fields = '__all__'